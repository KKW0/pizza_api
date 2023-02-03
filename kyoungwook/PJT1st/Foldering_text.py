import Foldering

sf = Foldering.FolderingFile()
sf.print_templates()
sf.template_name = 'kangkyoungwook1'
# sf.set_template()
data = sf.set_path('/home/rapa/project/avata/shot/boo/0010/plate/v001/boo_0010_plate_v001.0010.jpg')

print(data["project"])

# sf.add_template("kangkyoungwook3", '/home/rapa/project/{project}/shot/{seq}/{shot}/{dept}/{ver}/{seq}_{shot}_{dept}_{ver}.{padding}.{ext}')
