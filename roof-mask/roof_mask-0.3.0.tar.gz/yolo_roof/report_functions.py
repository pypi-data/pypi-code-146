### report ###
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

from yolo_roof.detect_functions import *
#### shapely ###
import shapely
import shapely.wkt
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPoint
from shapely.geometry import Polygon

## PDF
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

## ZIP
import zipfile

# email
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart

### Function for target address center lat long computation ###
def image_info_to_center_lat_lon(image_info, zoom, flag = 1):
    '''
    image_info is '[topleft tile x,
                    topleft tile y,
                    bottom right tile x,
                    bottom right tile y]'
    flag = 0 : NW-corner of the square
    flag = 1 : center
    flag = 2 : Other corner
    '''
    image_info_array = image_info.split(',')
    if flag == 0:
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]))//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]))//2
    
    elif flag == 1:
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]) + 1)//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]) + 1)//2

    elif flag ==2:
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]) + 2)//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]) + 2)//2
    else:
        print('flag is not defined. Using NW-corner of the square')
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]))//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]))//2

    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return [lat_deg, lon_deg]

def merge_polygones(image_folder,json_file,trainingDataset):
    allColors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (75,125,255), (125,75,255), (75,255,125), (125,255,75), (255,125,75), (255,75,125)]*8
    filename = str(uuid.uuid4())
    register_coco_instances(filename, {'thing_colors':allColors}, json_file, image_folder)
    metadata = MetadataCatalog.get(filename)
    dicts = DatasetCatalog.get(filename)
    model_folder = os.path.join(image_folder,'prediction_' + trainingDataset)
    print(f"Merging {trainingDataset} polygons")
    for dic in dicts:
        img = utils.read_image(dic["file_name"], "RGB")
        visualizer = Visualizer(img, metadata=metadata, instance_mode=ColorMode.SEGMENTATION)
        vis = visualizer.draw_dataset_dict(dic)
        out_filename = os.path.join(os.path.splitext(os.path.basename(dic["file_name"]))[0],trainingDataset +'_merged.jpg')
        
        out_filename2_extention = os.path.splitext(os.path.basename(dic["file_name"]))[1]
        out_filename2 = os.path.basename(dic["file_name"]).replace(out_filename2_extention,'_merged'+out_filename2_extention)
        vis.save(os.path.join(image_folder,out_filename))
        # vis.save(os.path.join(model_folder,out_filename2)) # model folder is not necessary
    print("Merging Finished.")
    return vis

def generate_referral_json(demoFolder, coco_json, new_cat, new_json_file_name):
    catIds = coco_json.getCatIds(catNms=[], supNms=[], catIds=[])
    # Obtain the category names
    categories = coco_json.loadCats(catIds)
    new_categories = [x['name'] for x in categories if x['name'] in new_cat]
    new_catIds = coco_json.getCatIds(catNms=new_categories, supNms=[], catIds=[])
    print(new_catIds)
    imgIds = coco_json.getImgIds()
    
    new_json_file = os.path.join(demoFolder, new_json_file_name)
    
    new_images = []
    new_annotations = []
    ann_id = 1
    new_image_id = 1

    for img_id in range(len(imgIds)):
        # get image information
        coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        annotations = coco_json.loadAnns(annIds)

        ann_start = ann_id
        for ann in annotations:
            # print(ann)
            # class selection
            if ann['category_id'] in new_catIds:
                
                # append annotation to coco jason file list
                new_annotations.append({"id": ann_id,
                                        "image_id": new_image_id,
                                        "category_id": ann['category_id'],
                                        "iscrowd": 0,
                                        # "area": ann['area'],
                                        # "bbox": ann['bbox'],
                                        "segmentation": ann['segmentation']
                                        })
                # get new annotation id
                ann_id += 1

        # get new image id
        new_image_id += 1
        # append image information to coco jason file list
        new_images.append(coco_img_info)

    info = {"year": 2022,
            "version": "1.0",
            "description": "Phase 2 data and coco json file",
            "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
            }

    json_data = {"info": info,
                 "categories": categories,
                 "images": new_images,
                 "annotations": new_annotations
                 }

    with open(new_json_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, sort_keys=True, indent=4)



def generate_referral_damage_json(demoFolder, coco_json, roof_boundary_json, new_cat, new_json_file_name):
    catIds = coco_json.getCatIds(catNms=[], supNms=[], catIds=[])
    # Obtain the category names
    categories = coco_json.loadCats(catIds)
    new_categories = [x['name'] for x in categories if x['name'] in new_cat]
    new_catIds = coco_json.getCatIds(catNms=new_categories, supNms=[], catIds=[])
    print(new_catIds)
    imgIds = coco_json.getImgIds()
    
    new_json_file = os.path.join(demoFolder, new_json_file_name)
    
    new_images = []
    new_annotations = []
    ann_id = 1
    new_image_id = 1

    for img_id in range(len(imgIds)):
        # get image information
        coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        annotations = coco_json.loadAnns(annIds)
        
        roof_poly = Polygon()
        # get image information
        coco_img_info = roof_boundary_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = roof_boundary_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        roof_annotations = roof_boundary_json.loadAnns(annIds)
        for ann in roof_annotations:
            for seg in ann['segmentation']:
                mask = np.array(seg).reshape(len(seg) // 2, 2)
                poly = Polygon(mask)
                roof_poly = roof_poly.union(poly)
        
        # roof_poly = roof_poly.buffer(-5.0)
        
        ann_start = ann_id
        for ann in annotations:
            # print(ann)
            # class selection
            if ann['category_id'] in new_catIds:
                current_poly = Polygon()
                for seg in ann['segmentation']:
                    mask = np.array(seg).reshape(len(seg) // 2, 2)
                    new_poly = Polygon(mask)
                    current_poly = current_poly.union(new_poly)

                if not current_poly.intersects(roof_poly):
                    continue
                else:
                    intersection_poly = current_poly.intersection(roof_poly)
                    
                if intersection_poly.geom_type == 'MultiPolygon':
                    for current_mask in intersection_poly:
                        if current_mask.area < 25:
                            continue
                        current_polygon_list = current_mask.exterior.coords
                        coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(current_mask.exterior.coords) * 2).tolist()
                        # append annotation to coco jason file list
                        new_annotations.append({"id": ann_id,
                                                "image_id": new_image_id,
                                                "category_id": ann['category_id'],
                                                "iscrowd": 0,
                                                # "area": ann['area'],
                                                # "bbox": ann['bbox'],
                                                "segmentation": coco_segmentation_format
                                                })
                        # get new annotation id
                        ann_id += 1
                elif intersection_poly.geom_type == 'Polygon':
                    if intersection_poly.area < 100:
                        continue
                    current_polygon_list = intersection_poly.exterior.coords
                    coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(current_polygon_list) * 2).tolist()
                    # append annotation to coco jason file list
                    new_annotations.append({"id": ann_id,
                                            "image_id": new_image_id,
                                            "category_id": ann['category_id'],
                                            "iscrowd": 0,
                                            # "area": ann['area'],
                                            # "bbox": ann['bbox'],
                                            "segmentation": coco_segmentation_format
                                            })
                    # get new annotation id
                    ann_id += 1             

        # get new image id
        new_image_id += 1
        # append image information to coco jason file list
        new_images.append(coco_img_info)

    info = {"year": 2022,
            "version": "1.0",
            "description": "Phase 2 data and coco json file",
            "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
            }

    json_data = {"info": info,
                 "categories": categories,
                 "images": new_images,
                 "annotations": new_annotations
                 }

    with open(new_json_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, sort_keys=True, indent=4)


class ReferralPoints:
    '''
    Read in referral rules and generate the csv format:
    Address    Total points    each referral elemten
      aaa          3              3  
    '''

    def __init__(self, referral_file, index):
        with open(referral_file) as f1:
            self.ref_json = json.load(f1)
        self.score = {'Address': index}
        self.score.update({'Total points': 0})
        self.score.update(dict((score_cat, 0) for score_cat in self.ref_json))
        self.score.update({'Roof area (pixels)': 0})

        self.score_cat = [x for x in self.ref_json]

        self.buffer = dict((score_cat,{'area_percentage': 0, 'count': 0}) for score_cat in self.ref_json)
        self.buffer.update({'Roof_boundary': 0})
        
        # print(self.score_cat)
        # print(self.buffer)

    def set_points(self, cat, points=0):
        self.score[cat] = points

    def update_total_points(self):
        for cat in self.score_cat:
            score = self.score[cat]
            self.score['Total points'] += score
            # print(f'{cat}:, {score}')

    def obtation_roof_boundary(self, predict_result,image_id):
        # get the image annotations ids
        annIds = predict_result.getAnnIds(imgIds=image_id)
        # get annotations from annotation ids
        annotations = predict_result.loadAnns(annIds)
        self.roof_poly = Polygon()
        for ann in annotations:
            for seg in ann['segmentation']:
                mask = np.array(seg).reshape(len(seg) // 2, 2)
                poly = Polygon(mask)
                self.roof_poly = self.roof_poly.union(poly)
                poly_area = poly.area
                self.buffer['Roof_boundary'] += poly_area
    
        ### compute roof area
        self.score['Roof area (pixels)'] = poly_area
        self.roof_poly = self.roof_poly.buffer(5.0) #add a buffer for HVAC which are located on the ground
        # aaa = self.buffer['Roof_boundary']
        # # print(poly)
        # print(f'roof {aaa*0.0002}')
        
    def update_buffer_value(self, predict_result, labels, image_id):
        # get the image annotations ids
        annIds = predict_result.getAnnIds(imgIds=image_id)
        # get annotations from annotation ids
        annotations = predict_result.loadAnns(annIds)
        # print(len(annotations))

        # update referral buffer
        for ann in annotations:
            if labels[ann['category_id']] in self.score_cat:
                                
                # if this instance is detected 'area_percentage' + current mask area
                for seg in ann['segmentation']:
                    mask = np.array(seg).reshape(len(seg) // 2, 2)
                    poly = Polygon(mask)
                    self.current_poly = poly
                    if not self.current_poly.intersects(self.roof_poly):
                        continue
                    poly_area = poly.area
                    poly_percentage = poly_area / (self.buffer['Roof_boundary'] + 1)
                    self.buffer[labels[ann['category_id']]]['area_percentage'] += poly_percentage
                    
                    # print(poly)
                    # class_label = labels[ann['category_id']]
                    # print(f'{class_label} poly_area {poly_area}')

                if not self.current_poly.intersects(self.roof_poly):
                    continue
                # if this instance is detected 'count' + 1
                self.buffer[labels[ann['category_id']]]['count'] += 1
                    
        # for each cat
        for referral_cat in self.score_cat:
            # for each value section
            for referral_value in self.ref_json[referral_cat]:
                # for each referral type
                for refferal_type in self.buffer[referral_cat]:
                    # print(refferal_type)
                    if refferal_type == referral_value['type']:
                        # if current value is not 0 and current value is in the value section
                        # and the new value is larger than the old value
                        # update the value
                        if self.buffer[referral_cat][refferal_type]!=0:
                            if referral_value['min'] <= self.buffer[referral_cat][refferal_type] < referral_value['max']:
                                if referral_value['point'] > self.score[referral_cat]:
                                    self.set_points(referral_cat, points=referral_value['point'])
                # print(referral_cat)
                # print(self.buffer[referral_cat])  

def generate_report(demoFolder):
    # demoFolder = 'roof_score_new_20230101'
    pred_damage_file = os.path.join(demoFolder,'prediction_Roof_damage/Roof_damage_all_in_one.json')
    pred_equip_file = os.path.join(demoFolder, 'prediction_Roof_equipment/Roof_equipment_all_in_one.json')
    pred_boundary_file =os.path.join(demoFolder, 'prediction_Roof_boundary/Roof_boundary_all_in_one.json')

    # read in referral rules and create corresponding functions
    referral_label_file = 'referral_labels_20221006.json'
    with open(referral_label_file) as f1:
        ref_json = json.load(f1)
    cat = [x for x in ref_json]
    # Load json file
    pred_damage = COCO(pred_damage_file)
    pred_equip = COCO(pred_equip_file)
    pred_boundary = COCO(pred_boundary_file)
    generate_referral_damage_json(demoFolder, pred_damage,pred_boundary,cat,'Referral_damage.json')
    generate_referral_json(demoFolder, pred_equip,cat,'Referral_equipment.json')
    vis_out = merge_polygones(demoFolder,os.path.join(demoFolder, 'Referral_damage.json'),'Damage')
    vis_out = merge_polygones(demoFolder,os.path.join(demoFolder, 'Referral_equipment.json'),'Equipment')

    ################################### Referral
    referral_output = []
    # Obtain the category ID numbers
    catIds = pred_damage.getCatIds()
    # Obtain the category names
    categories = pred_damage.loadCats(catIds)
    # Id2catname
    Damage_labels = [value['name'] for value in categories]

    # Obtain the category ID numbers
    catIds = pred_equip.getCatIds()
    # Obtain the category names
    categories = pred_equip.loadCats(catIds)
    # Id2catname
    Equipment_labels = [value['name'] for value in categories]

    for damage_img_id, equp_image_id in zip(pred_damage.getImgIds(), pred_equip.getImgIds()):
        assert pred_damage.loadImgs(damage_img_id) == pred_damage.loadImgs(equp_image_id)
        # get image information
        coco_img_info = pred_damage.loadImgs(damage_img_id)[0]
        address = os.path.splitext(coco_img_info['file_name'])[0]
        print(address)
        # zoom_level = int(address[-13:-11])

        # using :-14 to only keep address no zoom level and date
        # new_referral = ReferralPoints(referral_label_file, index=address[:-14])
        new_referral = ReferralPoints(referral_label_file, index=address) 

        # Roof Boundary
        # new_referral.buffer['Roof boundary'] = np.sqrt(coco_img_info['height'] * coco_img_info['width'])
        # new_referral.buffer['Roof_boundary'] = 0.5* coco_img_info['height'] * coco_img_info['width']
        # print(coco_img_info['height'] * coco_img_info['width'])
        new_referral.obtation_roof_boundary(pred_boundary, image_id = coco_img_info['id'])


        # Damage
        #################################################
        new_referral.update_buffer_value(pred_damage, Damage_labels, image_id = coco_img_info['id'] )
        # if zoom_level==22:
        #     print(new_referral.buffer['Roof_boundary']*0.0002)
        #     print(new_referral.buffer['Water pooling']['area_percentage']*new_referral.buffer['Roof_boundary']*0.0002)
        # else:
        #     print(new_referral.buffer['Roof_boundary']*0.00085)
        #     print(new_referral.buffer['Water pooling']['area_percentage']*new_referral.buffer['Roof_boundary']*0.00085)

        # Equipment
        #################################################
        new_referral.update_buffer_value(pred_equip, Equipment_labels, image_id = coco_img_info['id'])

        new_referral.update_total_points()
        referral_output.append(new_referral.score)
        df = pd.DataFrame.from_dict([new_referral.score])
        df.to_csv(os.path.join(demoFolder,address+'/referral.csv'), index=False, header=True)

    df = pd.DataFrame.from_dict(referral_output)
    df.to_csv(os.path.join(demoFolder,'all_referral.csv'), index=False, header=True)
    image_csv = pd.read_csv(os.path.join(demoFolder,"image.csv"))
    referral_csv = pd.read_csv(os.path.join(demoFolder,"all_referral.csv"))

    image_csv.merge(referral_csv,how='outer',on='Address').to_csv(os.path.join(demoFolder, 'all_address.csv'), index=False, header=True)

    ################################################################# PDF
    image_csv = pd.read_csv(os.path.join(demoFolder,'image.csv'))
    referral_csv = pd.read_csv(os.path.join(demoFolder,'all_referral.csv'))
    all_address_csv = pd.read_csv(os.path.join(demoFolder, 'all_address.csv'))
    # Today_date = datetime.today().strftime('%Y-%m-%d')
    # # print(Today_date)
    full_address = all_address_csv["Address"].tolist()
    insured_name = all_address_csv["InsuredName"].tolist()
    image_date = all_address_csv["Image date"].tolist()
    image_info = all_address_csv["Image info"].tolist()
    zoom_level = all_address_csv["Image level"].tolist()

    key_name = all_address_csv.columns
    key_name_index = all_address_csv.columns.get_loc('Total points')
    gsd_key = all_address_csv.columns.get_loc('Image gsd (meters/pixels)')
    pixels_area_key = all_address_csv.columns.get_loc('Roof area (pixels)')
    # print(key_name[key_name_index])

    for address_index in range(len(full_address)):
        address = full_address[address_index]
        row = all_address_csv.iloc[address_index]
        print(f'index:{address_index}, address:{address}')
        if np.isnan(row[key_name_index]):
            continue
        # initializing variables with values
        url_zoom_level = zoom_level[address_index]
        cat_lon_coord = image_info_to_center_lat_lon(image_info[address_index], url_zoom_level)
        url_lat = cat_lon_coord[0]
        url_lon = cat_lon_coord[1]
        url_date = image_date[address_index].replace('-','')
        url = f'https://apps.nearmap.com/maps/#/@{url_lat},{url_lon},{url_zoom_level}z,0d/V/{url_date}'

        fileName = os.path.join(demoFolder,address+'.pdf')
        documentTitle = f'Refferal'
        title = f'{insured_name[address_index]}'
        subTitle = address

        Damage_image_name = os.path.join(demoFolder,address+'/Damage_merged.jpg')
        Equipment_image_name = os.path.join(demoFolder,address+'/Equipment_merged.jpg')

        pdf = canvas.Canvas(fileName)
        pdf.setTitle(documentTitle)
        pdf.setFont("Times-Roman", 14)
        pdf.drawCentredString(300, 800, title)

        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Times-Roman", 12)
        pdf.drawCentredString(290, 770, subTitle)

        # drawing a line
        pdf.line(30, 760, 550, 760)

        # information
        text = pdf.beginText(40, 740)
        text.setFont("Courier", 12)
        text.setFillColor(colors.black)
        text.textLine(f'Image date: {image_date[address_index]}')

        ######################################### 100 points
        # Range	    3	   3	        3	          3	                 3	           1	       3
        # weight	1	   2.5	        2.5	          1	                 1	           1	       1
        # Other damage	Staining	Water pooling	Skylight	HVAC/Cooling tower	Pipeline	Solar panel


        total_point = 0
        if row[key_name_index]!=0:
            for i in range(key_name_index+1, len(key_name)):
                if key_name[i] == 'Other damage':
                    total_point += row[i]*1
                elif key_name[i] == 'Staining':
                    total_point += row[i]*2.5
                elif key_name[i] == 'Water pooling':
                    total_point += row[i]*2.5
                elif key_name[i] == 'Skylight':
                    total_point += row[i]*1
                elif key_name[i] == 'HVAC/Cooling tower':
                    total_point += row[i]*1
                elif key_name[i] == 'Pipeline':
                    total_point += row[i]*1
                elif key_name[i] == 'Solar panel':
                    total_point += row[i]*1
            total_point = 100 - total_point * 5
            if total_point> 0 :
                line= f'Total scores: {total_point}'
                text.textLine(line)
                text.setFillColor(colors.blue)
            else:
                line = 'Total scores: 0'
                text.textLine(line)
                text.setFillColor(colors.blue)
        else:
            line = 'Total scores: 100'
            text.textLine(line)
            text.setFillColor(colors.blue)

        for i in range(key_name_index+1, len(key_name)):
            if i == pixels_area_key:
                gsd_area = row[gsd_key] * row[gsd_key] * row[pixels_area_key]
                text.textLine(f'Roof area: {int(gsd_area)} m\u00b2')
                continue
            if int(row[i]) == 0:
                line = key_name[i] + ': ' + 'Not detected'
                text.textLine(line)
            elif int(row[i]) == 1:
                if key_name[i] == 'Pipline' or 'Solar panel': 
                    line = key_name[i] + ': ' + 'Detected'
                    text.textLine(line)
                    continue
                if key_name[i] == 'Staining' or 'Water pooling' or 'Other damage':
                    line = key_name[i] + ': ' + 'Minor'
                    text.textLine(line)
                    continue
                if key_name[i] == 'Skylight' or 'HVAC/Cooling tower':
                    line = key_name[i] + ': ' + 'Minimal'
                    text.textLine(line)
                    continue
            elif int(row[i]) == 2:
                if key_name[i] == 'Pipline' or 'Solar panel': 
                    line = key_name[i] + ': ' + 'Detected'
                    text.textLine(line)
                    continue
                if key_name[i] == 'Staining' or 'Water pooling' or 'Other damage':
                    line = key_name[i] + ': ' + 'Moderate'
                    text.textLine(line)
                    continue
                if key_name[i] == 'Skylight' or 'HVAC/Cooling tower':
                    line = key_name[i] + ': ' + 'A few'
                    text.textLine(line)
                    continue
            else:
                if key_name[i] == 'Pipline' or 'Solar panel': 
                    line = key_name[i] + ': ' + 'Detected'
                    text.textLine(line)
                    continue
                if key_name[i] == 'Staining' or 'Water pooling' or 'Other damage':
                    line = key_name[i] + ': ' + 'Major'
                    text.textLine(line)
                    continue
                if key_name[i] == 'Skylight' or 'HVAC/Cooling tower':
                    line = key_name[i] + ': ' + 'Many'
                    text.textLine(line)
                    continue

        pdf.drawText(text)
    ################################################## 19 points
        # if row[key_name_index]!=0:
        #     line= f'Total points: {int(row[key_name_index])}'
        #     text.textLine(line)
        # else:
        #     line = 'Total points: 0'
        #     text.textLine(line)
        # for i in range(key_name_index+1, len(key_name)):
        #     if row[i]>0:
        #         line = key_name[i] + ': ' + str(int(row[i]))
        #         text.textLine(line)
        # pdf.drawText(text)
    ##########################################################

        # images
        textLines = ['Image',
                    'Damage',
                    'Equipment'
        ]
        image_name = address + '.jpg'
        image_full_name = os.path.join(demoFolder,image_name)

        image = cv2.imread(image_full_name)
        height = image.shape[0]
        width = image.shape[1]
        ratio = width/height

        if height < width: # height < width horizontal
            tmp_width = 350
            tmp_height = 180
            new_width = ratio * tmp_height
            if new_width > tmp_width:
                draw_width = tmp_width
                draw_height = draw_width/ratio
            else:
                draw_width = new_width
                draw_height = tmp_height
            text = pdf.beginText(100, 500)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-3])
            pdf.drawText(text)
            pdf.drawInlineImage(image_full_name, 200, 440, width = draw_width, height = draw_height)
            pdf.linkURL(url, (200, 440, 200+draw_width, 440+draw_height), relative=1)
    # https://apps.nearmap.com/maps/#/@30.6622190,-88.1816001,20.00z,0d/V/20220110

            text = pdf.beginText(100, 300)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-2])
            pdf.drawText(text)
            pdf.drawInlineImage(Damage_image_name, 200, 240, width = draw_width, height = draw_height)
            pdf.linkURL(url, (200, 240, 200+draw_width, 240+draw_height), relative=1)


            text = pdf.beginText(100, 100)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-1])
            pdf.drawText(text)
            pdf.drawInlineImage(Equipment_image_name, 200, 40, width = draw_width, height = draw_height)
            pdf.linkURL(url, (200, 40, 200+draw_width, 40+draw_height), relative=1)

        else: # vertical
            tmp_width = 250
            tmp_height = 300
            new_width = ratio * tmp_height
            if new_width > tmp_width:
                draw_width = tmp_width
                draw_height = draw_width/ratio
            else:
                draw_width = new_width
                draw_height = tmp_height
            text = pdf.beginText(310, 370)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-3])
            pdf.drawText(text)
            pdf.drawInlineImage(image_full_name, 310, 380, width = draw_width, height = draw_height)
            pdf.linkURL(url, (310, 380, 310+draw_width, 380+draw_height), relative=1)

            text = pdf.beginText(40, 30)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-2])
            pdf.drawText(text)
            pdf.drawInlineImage(Damage_image_name, 40, 40, width = draw_width, height = draw_height)
            pdf.linkURL(url, (40, 40, 40+draw_width, 40+draw_height), relative=1)


            text = pdf.beginText(310, 30)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-1])
            pdf.drawText(text)
            pdf.drawInlineImage(Equipment_image_name, 310, 40, width = draw_width, height = draw_height)
            pdf.linkURL(url, (310, 40, 310+draw_width, 40+draw_height), relative=1)


        # saving the pdf
        pdf.save()

def zip_download_file(image_folder_name):
    ############################## ZIP
    # excel_file_path = "roof_score_new_20220803.csv"
    # excel_file_path = "roof_score_new_20220726.csv"
    # image_folder_name = os.path.splitext(os.path.basename(excel_file_path))[0]

    # import glob
    # jpgFilenamesList = glob.glob(image_folder_name + '/*.jpg')
    # pdfFilenamesList = glob.glob(image_folder_name + '/*.pdf')
        # for f in jpgFilenamesList:   
        #     myzip.write(f)
        # for f in pdfFilenamesList:   
        #     myzip.write(f)

    def zipdir(path, ziph):
        file_path = os.path.join(image_folder_name, path)
        # ziph is zipfile handle
        if not os.path.isdir(file_path):
            if path[-3:]=='jpg': # move the orignial image to image folder
                ziph.write(file_path,path.replace('.jpg','/Image.jpg'))
            else:
                ziph.write(file_path, path)
        else:
            for root, dirs, files in os.walk(file_path):           
                for file in files:
                    if file[0:4] != 'Roof': # don't include the roof boundary model
                        ziph.write(os.path.join(root, file), os.path.join(path, file))


    file_list = [f for f in os.listdir(image_folder_name) if f[0].isnumeric()]
    print('Zipping')
    with zipfile.ZipFile(os.path.join(image_folder_name, 'roof.zip'), 'w') as myzip:
        myzip.write(os.path.join(image_folder_name, 'all_address.csv'), 'all_address_' + image_folder_name[-8:] + '.csv')
        for f in file_list:    
            zipdir(f, myzip)
    print('Zipping Done')

def send_email(receiver_email, address):
    host_server = 'smtp.qq.com'
    sender_qq = '1303242060'
    pwd = 'fhzevydopuvagfae'
    # pwd = input('Please input the password (not the login pwd)')

    sender_qq_mail = '1303242060@qq.com'
    # receiver = 'ruixu_liu@cinfin.com'

    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(0)   # 1 for debug
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)


    msg = MIMEMultipart() # .txt .jpg .xls
    mail_title = 'Roof condition file'
    mail_content = address
    msg.attach(MIMEText(mail_content,'plain','utf-8'))

    # Add attachment
    att1=MIMEText(open('roof_score_new_20230101/roof.zip','rb').read(),'base64','utf-8')  #open file
    att1['Content-Type']='application/octet-stream' 
    att1['Content-Disposition']='attachment;filename=roof.zip'  

    # att2=MIMEText(open('aaa.jpg','rb').read(),'base64','utf-8')
    # att2['Content-Type']='application/octet-stream'
    # att2['Content-Disposition']='attachment;filename=aaa.jpg' 
    msg.attach(att1)
    # msg.attach(att2)

    print('Preparing done.')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver_email

    smtp.sendmail(sender_qq_mail, receiver_email, msg.as_string())

    smtp.quit()
    print('Finish send email.')
