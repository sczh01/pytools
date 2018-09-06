from PIL import Image  
from PIL import ImageDraw


def ellipse_with_angle(im,x,y,major,minor,angle,color):
    # take an existing image and plot an ellipse centered at (x,y) with a
    # defined angle of rotation and major and minor axes.
    # center the image so that (x,y) is at the center of the ellipse
    x -= int(major/2)
    y -= int(major/2)

    # create a new image in which to draw the ellipse
    im_ellipse = Image.new('RGBA', (major,major), (255,255,255,0))
    draw_ellipse = ImageDraw.Draw(im_ellipse, "RGBA")

    # draw the ellipse
    ellipse_box = (0,int(major/2-minor/2),major,int(major/2-minor/2)+minor)
    draw_ellipse.ellipse(ellipse_box, fill=color)

    im_ellipse.save("test.bmp")
   # rotate the new image
    rotated = im_ellipse.rotate(angle)
    im_ellipse.save("test-1.bmp")

    rx,ry = rotated.size

    # paste it into the existing image and return the result
    im.paste(rotated, (x,y,x+rx,y+ry), mask=rotated)
    return im

def print_param_1(x,y,z=3,*poster,**keypar):
    print(x,y,z)
    print(poster)
    for i in range(len(poster)):
        print(poster[i])
    print(keypar)

if __name__ == '__main__':
    print_param_1(1,2,3,5,6,7,foo=1,bar="22")
    print_param_1(444,555,65,6,7,8,'sec_1','sec_2',foo=1, last='last_p')

    im=Image.open("1.bmp")
    ellipse_with_angle(im,200,1200,200,150,20,(255,0,255))
    im.save("1-1.bmp")