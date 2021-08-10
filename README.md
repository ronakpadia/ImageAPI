# ImageAPI

An Flask based API which uses POST request to manipulate image(crop/rotate) and match strings using fuzzywuzzy

API endpoint(/rotate)POST
- Headers = Content-type:multipart/form-data
- form-data = {'degrees': 40, 'files': xyz.jpg}

API endpoint(/crop)POST
- Headers = Content-type:multipart/form-data
- form-data = {'x1':0, 'y1':0, 'x2':500, 'y2':500, 'files': xyz.jpg}

API endpoint(/name)POST
- form-data = {'string1': "Hello", 'string2': "Hello!!"}
