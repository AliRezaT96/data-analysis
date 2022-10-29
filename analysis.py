def num_val_for_attr(df):
    model = 0
    origin = 0
    texture = 0
    color = 0
    size = 0
    price = 0
    quality = 0
    weight = 0
    style = 0
    sex = 0
    brand = 0
    loc = 0
    season = 0
    product = 0
    
    for i in range(len(df)):
        if df.attribute[i] == 'مدل و نوع':
            model+=1
        elif df.attribute[i] == 'اصالت':
            origin+=1
        elif df.attribute[i] == 'جنس':
            texture+=1
        elif df.attribute[i] == 'رنگ':
            color+=1
        elif df.attribute[i] == 'سایز':
            size+=1
        elif df.attribute[i] == 'قیمت':
            price+=1
        elif df.attribute[i] == 'کیفیت':
            quality+=1
        elif df.attribute[i] == 'وزن':
            weight+=1
        elif df.attribute[i] == 'استایل':
            style+=1
        elif df.attribute[i] == 'جنسیت':
            sex+=1
        elif df.attribute[i] == 'برند':
            brand+=1
        elif df.attribute[i] == 'مکان':
            loc+=1
        elif df.attribute[i] == 'فصل':
            season+=1
        elif df.attribute[i] == 'محصول':
            product+=1
    
    attribute_counts = {
        'مدل و نوع': model,
        'اصالت': origin,
        'جنس': texture,
        'رنگ': color,
        'سایز': size,
        'قیمت': price,
        'کیفیت': quality,
        'وزن': weight,
        'استایل': style,
        'جنسیت': sex,
        'برند': brand,
        'مکان': loc,
        'فصل': season,
        'محصول': product,
    }
    
    return attribute_counts


def generate_N_grams(text,ngram):
    words=[word for word in text.split(" ")]
    temp=zip(*[words[i:] for i in range(0,ngram)])
    ans=[' '.join(ngram) for ngram in temp]
    return ans
    