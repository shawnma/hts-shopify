from PIL import Image, ImageDraw, ImageFont
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEFAULT_CONFIG = {
    'font-size': 100,
    'color': [0,0,0,255], # black
    'type' : 'JPeG',
    'start': [10,10],
    'quality' : 95,
    'limit' : [200, 200],
    'font' : FONT,
    'align' : 'center'
}

def calc_text_block_size(text, font_file, font_size):
    w = h = 0
    font = ImageFont.truetype(font_file, font_size)
    for l in text.split("\n"):
        size = font.getsize(l)
        w = max(size[0], w)
        h += size[1]
    return (w, h)

def determine_font_size(text, config):
    exp_width = config['limit'][0] - config['start'][0]
    exp_height = config['limit'][1] - config['start'][1]
    (w, h) = calc_text_block_size(text, config['font'], config['font-size']) 
    ratio = max(1.0*w/exp_width, 1.0*h/exp_height)
    #print ratio, config['font-size']/ratio
    new_size = int(config['font-size']/ratio)
    while new_size > 6:
        (w, h) = calc_text_block_size(text, config['font'], new_size)
        #print new_size, w, h, exp_width, exp_height
        if w < exp_width and h < exp_height:
            break
        new_size = new_size - 1
    return ImageFont.truetype(config['font'], new_size)

def draw(orig, text, dest, config = DEFAULT_CONFIG):
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(config)
    #print cfg
    text = text.replace('\r', '', 100)
    image = Image.open(orig)
    d = ImageDraw.Draw(image)
    font = determine_font_size(text, cfg)
    d.multiline_text(tuple(cfg['start']), text, tuple(cfg['color']), font, align=cfg['align'])
    #d.rectangle([tuple(cfg['start']),tuple(cfg['limit'])], outline=(255,0,0))
    image.save(dest, cfg['type'], quality=cfg['quality'])

if __name__ == '__main__':
    draw('slide_2.jpg', "hello\n,\n world\nTo my dear", "new.jpg", {'limit': [582,142], 'start': [354,41], 'align':'right'})
