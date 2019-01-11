def cyrilicToLatin(value):

    if any(c in "абвгдђежзијклљмнњопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ" for c in value):
        retVal = value
        
        retVal = retVal.replace('а', 'a')
        retVal = retVal.replace('б', 'b')
        retVal = retVal.replace('в', 'v')
        retVal = retVal.replace('г', 'g')
        retVal = retVal.replace('д', 'd')
        retVal = retVal.replace('ђ', 'đ')
        retVal = retVal.replace('е', 'e')
        retVal = retVal.replace('ж', 'ž')
        retVal = retVal.replace('з', 'z')
        retVal = retVal.replace('и', 'i')
        retVal = retVal.replace('ј', 'j')
        retVal = retVal.replace('к', 'k')
        retVal = retVal.replace('л', 'l')
        retVal = retVal.replace('љ', 'lj')
        retVal = retVal.replace('м', 'm')
        retVal = retVal.replace('н', 'n')
        retVal = retVal.replace('њ', 'nj')
        retVal = retVal.replace('о', 'o')
        retVal = retVal.replace('п', 'p')
        retVal = retVal.replace('р', 'r')
        retVal = retVal.replace('с', 's')
        retVal = retVal.replace('т', 't')
        retVal = retVal.replace('ћ', 'ć')
        retVal = retVal.replace('у', 'u')
        retVal = retVal.replace('ф', 'f')
        retVal = retVal.replace('х', 'h')
        retVal = retVal.replace('ц', 'c')
        retVal = retVal.replace('ч', 'č')
        retVal = retVal.replace('џ', 'dž')
        retVal = retVal.replace('ш', 'š')
        
        retVal = retVal.replace('А', 'A')
        retVal = retVal.replace('Б', 'B')
        retVal = retVal.replace('В', 'V')
        retVal = retVal.replace('Г', 'G')
        retVal = retVal.replace('Д', 'D')
        retVal = retVal.replace('Ђ', 'Đ')
        retVal = retVal.replace('Е', 'E')
        retVal = retVal.replace('Ж', 'Ž')
        retVal = retVal.replace('З', 'Z')
        retVal = retVal.replace('И', 'I')
        retVal = retVal.replace('Ј', 'J')
        retVal = retVal.replace('К', 'K')
        retVal = retVal.replace('Л', 'L')
        retVal = retVal.replace('Љ', 'Lj')
        retVal = retVal.replace('М', 'M')
        retVal = retVal.replace('Н', 'N')
        retVal = retVal.replace('Њ', 'Nj')
        retVal = retVal.replace('О', 'O')
        retVal = retVal.replace('П', 'P')
        retVal = retVal.replace('Р', 'R')
        retVal = retVal.replace('С', 'S')
        retVal = retVal.replace('Т', 'T')
        retVal = retVal.replace('Ћ', 'Ć')
        retVal = retVal.replace('У', 'U')
        retVal = retVal.replace('Ф', 'F')
        retVal = retVal.replace('Х', 'H')
        retVal = retVal.replace('Ц', 'C')
        retVal = retVal.replace('Ч', 'Č')
        retVal = retVal.replace('Џ', 'Dž')
        retVal = retVal.replace('Ш', 'Š')
        return retVal
    
    return value

def serbianLatinToLatin(value):

    if any(c in "đžćčšĐŽĆČŠ" for c in value):
        retVal = value

        retVal = retVal.replace('đ', 'dj')
        retVal = retVal.replace('ž', 'z')
        retVal = retVal.replace('ć', 'c')
        retVal = retVal.replace('č', 'c')
        retVal = retVal.replace('š', 's')

        retVal = retVal.replace('Đ', 'Dj')
        retVal = retVal.replace('Ž', 'Z')
        retVal = retVal.replace('Ć', 'C')
        retVal = retVal.replace('Č', 'C')
        retVal = retVal.replace('Š', 'S')
        return retVal
    
    return value
