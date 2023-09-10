import json
from apps.server.models import Info, ImageModel, Annotation, Category, COCOData, Tasks
from apps.utils import set_info, get_timestamp, get_categories

async def postprocess_data(pk_of_dataset, data, mongodb ):
    data_dict = data
    data_dict['_id'] = str(data_dict['_id'])
    task = Tasks(**data_dict)
    file_path = './inputs/'+ task.video_file

    document = COCOData()

    # TODO: fill dataset info attributes if will have spare time
    info = set_info( video_name = task.video_file, video_height = 480, video_width = 640, video_fps = 30, video_length = 0)
    
    

    try:
        pass
        # process video (we have file_path to video) and get segmentation masks

    except Exception as e:
        status = 'E'
        message = 'Ошибка обработки этапа 1:' + str(e)
        return (-1, status, message)
    
    processed_segmentations = [[[10.0 , 12.0, 11.0, 14.0, 15.0, 16.0]],[[10.0 , 12.0, 11.0, 14.0, 15.0, 16.0]]]
    processed_images = ['fileN1.jpg','fileN2.jpg']
    gps_coords = [[55,44],[68,55]]
    i: int = 0
    
    document_annotations = []
    document_images = []

    for segmentation, image, gps in zip(processed_segmentations,processed_images,gps_coords):

        annotation_model = Annotation(
            segmentation = segmentation,
            id = i,
            image_id = i
            )
        image_model = ImageModel(
            id = i,
            license = 0,
            frame_id = i,
            date_captured = get_timestamp(),
            gps_coord = gps,
            file_name = image
        )

        
        document_annotations.append(annotation_model)
        document_images.append(image_model)

    document.annotations = document_annotations
    document.images = document_images
    document.info = info
    document.categories = get_categories()


    
    doc_dict = document.model_dump()
    collection = mongodb['coco_data']
    
    # comment if we need to insert, not update
    result = await collection.replace_one({"_id": pk_of_dataset}, doc_dict)
    pk_of_dataset = 1
    #result = await collection.insert_one(doc_dict)
    #pk_of_dataset = result.inserted_id

    status = 'S' # or E if error
    message = 'Обработка завершена'
    return (pk_of_dataset, status, message)
