#!/bin/bash
#mongoimport --uri "mongodb://mongoadmin:secret@localhost:27017/road_defects" --collection "coco_data" --file ./assets/import.json
sudo docker exec -i mongo_db sh -c 'mongoimport --uri "mongodb://mongoadmin:secret@localhost:27017/road_defects?authSource=admin" --collection coco_data ' < ./assets/import.json