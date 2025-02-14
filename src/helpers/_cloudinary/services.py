from django.conf import settings
from django.template.loader import get_template

# for image
def get_cloudinary_image_object(
                                instance, # self/obj
                                field_name="image",
                                as_html=False,
                                width=1200
                            ):
    if not hasattr(instance, field_name):
        return "" 
    image_object = getattr(instance, field_name) # give the value of instance fielsname if match with inatance                    
    if not image_object:
        return ""
    image_options = {
        "width": width
    }
    if as_html:
        return image_object.image(**image_options)
    url = image_object.build_url(**image_options)
    return url


    
'''
    -- old code 
def get_cloudinary_image_object(
                                instance, 
                                field_name="image",
                                as_html=False,
                                width=1200
                            ):
    if not instance.image:
        return ""
    image_options = {
        "width": width
    }
    if as_html:
        return instance.image.image(**image_options)
    url = instance.image.build_url(**image_options)
    return url
''' 


# for video
def get_cloudinary_video_object(
                                instance, # self/obj
                                field_name="video",
                                as_html=False,
                                width=None,
                                height=None,
                                sign_url=False, # for private videos 
                                fetch_format="auto", # is for cloudinary automaticlly detemine best formate for media delivere. 
                                quality="auto",
                                controls=True,
                                autoplay=True,
                                bigPlayButton=True,
                                seekThumbnails=False,
                                aiHighlightsGraph=True
                            ): # parameter just for change value of video_option dynamocally 
    if not hasattr(instance, field_name):
        return "" 
    video_object = getattr(instance, field_name) # give the value of instance fielsname if match with inatance                    
    if not video_object:
        return ""
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "controls": controls,
        "autoplay": autoplay,
        "bigPlayButton": bigPlayButton,
        "seekThumbnails": seekThumbnails,
        "aiHighlightsGraph": True
    }
    if width is not None:
        video_options['width'] = width
    if height is not None:
        video_options['height'] = height
    if height and width:
        video_options['crop'] = "limit" # crop limit specife the size of image or video
    url = video_object.build_url(**video_options) # video_object.video(**video_options) -> return video  html tags. build_url return url of video. 
    if as_html:
        templates_name = "videos/snipper/embed.html" # path template 
        tmpl = get_template(templates_name) # get_tamplate take path of template as an argument and then parse the template file and return template object. that here store in tmpl.  
        _html = tmpl.render({'video_url': url, "cloud_name": settings.CLOUDINARY_CLOUD_NAME, 'base_color': "#007cae"}) # then render() fn render that context in embed.html page or we can access this data in embed.html page 
        return _html # then we return _html. so we get value of embed.html in where we call get_cloudinary_video_object 
    return url