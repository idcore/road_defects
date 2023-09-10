import open3d as o3d
import numpy as np
import open3d as o3d
import os
import glob
import re
import pandas as pd
import glob

FRAMES = 30
directory = r"E:\NN_defects_road_2023\NN_defects_road_2023\data\train_dataset\clear_data\__points"
gps = r'C:\Users\Heinrich\Desktop\hacka\points_geo.csv'

def read_point_cloud_from_file(file_path, point_step=48):
    with open(file_path, 'rb') as f:
        binary_data = f.read()


    points_np = np.frombuffer(binary_data, dtype=np.uint8)
    reshaped_points = points_np.reshape(-1, point_step)

    x = np.frombuffer(reshaped_points[:, 0:4].tobytes(), dtype=np.float32)
    y = np.frombuffer(reshaped_points[:, 4:8].tobytes(), dtype=np.float32)
    z = np.frombuffer(reshaped_points[:, 8:12].tobytes(), dtype=np.float32)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(np.array([x, y, z]).T)
    
    # Статистическое удаление выбросов
    point_cloud, ind = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    
    return point_cloud


def nearest_neighbors_kdtree(kdtree, query_points):
    nearest_indices = []
    for point in query_points:
        [_, idx, _] = kdtree.search_knn_vector_3d(point, 1)
        nearest_indices.append(idx[0])
    return np.array(nearest_indices)

file_names = glob.glob(os.path.join(directory, '*.bin'))

file_names = sorted(file_names, key=lambda x: int(re.search(r'rowid_(\d+)', x).group(1)))

combined_pcd = read_point_cloud_from_file(file_names[0])

for i in range(0, len(file_names), FRAMES):
    chunk_files = file_names[i:i+FRAMES]
    df = pd.read_csv(gps)
    latitude_list = []
    longitude_list = []
    altitude_list = []

    combined_pcd = read_point_cloud_from_file(chunk_files[0])
    
    for file_name in chunk_files[1:]:
        next_pcd = read_point_cloud_from_file(file_name)
        
        df['points_file_path'] = df['points_file_path'].str.split('/').str[-1]
        df['geo_file_path'] = df['geo_file_path'].str.split('/').str[-1]
        file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
        new_file_name = f"{file_name_without_extension}.json"

        latitude = df[df['points_file_path']==new_file_name]['latitude']
        longitude = df[df['points_file_path']==new_file_name]['longitude']
        altitude = df[df['points_file_path']==new_file_name]['altitude']
        latitude_list.append(float(latitude))
        longitude_list.append(float(longitude))
        altitude_list.append(float(altitude))

        # Применяем алгоритм ICP для соединения облаков
        threshold = 1.0  # максимальное расстояние для "совмещения" точек
        trans_init = np.asarray([[1, 0, 0, 0],  # идентичное преобразование
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])
        
        reg_p2p = o3d.pipelines.registration.registration_icp(
            next_pcd, combined_pcd, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())
        
        next_pcd.transform(reg_p2p.transformation)
        
        combined_pcd += next_pcd

    point_cloud = combined_pcd

    average_latitude = latitude_list[-1]
    average_longitude = longitude_list[-1]
    average_altitude = altitude_list[-1]

    # Используем RANSAC для нахождения плоскости
    plane_model, inliers = point_cloud.segment_plane(distance_threshold=0.1,
                                                    ransac_n=50,
                                                    num_iterations=4000)

    # `plane_model` содержит коэффициенты плоскости в форме [a, b, c, d]
    # для уравнения плоскости ax + by + cz + d = 0
    a, b, c, d = plane_model

    # Нормаль к плоскости
    plane_normal = np.array([a, b, c])

    # Нормализуем нормаль
    plane_normal = plane_normal / np.linalg.norm(plane_normal)

    # Находим вектор вращения и угол между нормалью к плоскости и осью Z
    axis = np.cross(plane_normal, [0, 0, 1])
    axis = axis / np.linalg.norm(axis)
    angle = np.arccos(np.dot(plane_normal, [0, 0, 1]))

    # Создаем матрицу вращения
    R = o3d.geometry.get_rotation_matrix_from_axis_angle(axis * angle)

    # Применяем вращение к облаку точек
    point_cloud.rotate(R, center=(0, 0, 0))

    points_cloud = np.asarray(point_cloud.points)

    z_coordinates = points_cloud[:, 2]  # Извлекаем z-координаты

    # Определяем минимальное и максимальное значения Z для определения границ бакетов
    z_min = np.min(z_coordinates)
    z_max = np.max(z_coordinates)

    # Создаем 40 бакетов
    num_buckets = 40
    buckets = np.linspace(z_min, z_max, num_buckets + 1)

    # Разделяем точки по бакетам
    bucket_indices = np.digitize(z_coordinates, buckets)

    # Подсчитываем количество точек в каждом бакете
    counts = np.bincount(bucket_indices)

    co= 0
    # Выводим количество точек и границы каждого бакета
    for i in range(1, len(buckets)): 
        count = counts[i] if i < len(counts) else 0  # На случай, если нет точек в последнем бакете
        if count > co:
            co = count
            lower_bound = buckets[i - 1]
            upper_bound = buckets[i]

    new_point_cloud = o3d.geometry.PointCloud()

    filtered_points_array = points_cloud[points_cloud[:, 2] <= upper_bound]

    new_point_cloud.points = o3d.utility.Vector3dVector(filtered_points_array)

    points_cloud = np.asarray(new_point_cloud.points)

    #Кластеризация
    # 1. Семплирование
    sample_indices = np.random.choice(points_cloud.shape[0], size=int(points_cloud.shape[0]*0.1), replace=False)
    sampled_points = points_cloud[sample_indices]

    # 2. Кластеризация семпла
    sample_point_cloud = o3d.geometry.PointCloud()
    sample_point_cloud.points = o3d.utility.Vector3dVector(sampled_points)
    labels = np.array(sample_point_cloud.cluster_dbscan(eps=0.2, min_points=20, print_progress=True))

    # 3. Присвоение меток остальным точкам
    kdtree = o3d.geometry.KDTreeFlann(sample_point_cloud)
    labels_all = labels[nearest_neighbors_kdtree(kdtree, points_cloud)]

    # Сдвигаем все метки на 1, чтобы избавиться от отрицательных значений
    adjusted_labels = labels_all + 1

    # Подсчет количества точек в каждом кластере
    cluster_counts = np.bincount(adjusted_labels)

    # Находим индекс кластера с самым большим количеством точек
    largest_cluster_idx = np.argmax(cluster_counts[1:]) + 1

    # Фильтрация точек, чтобы оставить только точки из самого большого кластера
    largest_cluster_points = points_cloud[adjusted_labels == largest_cluster_idx]

    z_coords = largest_cluster_points[:, 2]

    mean_z = np.mean(z_coords)
    std_dev = np.std(z_coords)
    threshold = mean_z - 5 * std_dev  # 5 сигм

    # Выделите точки, которые отклоняются на 5 сигм от среднего значения
    outliers = [point for point in largest_cluster_points if point[2] < threshold]

    # Создаем облако точек для выбросов
    outliers_cloud = o3d.geometry.PointCloud()
    outliers_cloud.points = o3d.utility.Vector3dVector(outliers)

    # Применяем DBSCAN для выделения кластеров среди выбросов
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(outliers_cloud.cluster_dbscan(eps=0.05, min_points=5, print_progress=True))
        if np.all(labels != -1):
            #КУДА ТО ВОЗВРАЩАТЬ
            print(average_latitude, average_longitude, average_altitude)