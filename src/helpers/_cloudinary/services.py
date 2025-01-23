from django.conf import settings
from django.template.loader import get_template

# for image
def get_cloudinary_image_object(
                                instance, 
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

video_html = """
    <video controls autoplay bigPlayButton>
        <source src="{video_url}"></source>
    </video>
"""

# for video
def get_cloudinary_video_object(
                                instance, 
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
    video_objest = getattr(instance, field_name) # give the value of instance fielsname if match with inatance                    
    if not video_objest:
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
        video_options['crop'] = "limit"
    url = video_objest.build_url(**video_options)
    if as_html:
        templates_name = "videos/snipper/embed.html" # path template 
        tmpl = get_template(templates_name) # get_tamplate take path of template as an argument and then parse the template file and return template object. that here store in tmpl.  
        _html = tmpl.render({'video_url': url, "cloud_name": settings.CLOUDINARY_CLOUD_NAME, 'base_color': "#007cae"}) # get_template give us an method name is render to generate html tags in string with context with httpResponse. So render fun. render context data in embed.html page so in embed.html page we can access video url using {{ video_url }} like that. 
        return _html # then we return _html. so we get value of embed.html in where we call get_cloudinary_video_object 
    return url