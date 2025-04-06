def section_scales(chosen_geoscale, df):
        # Ecclesiastical
    if chosen_geoscale == 'Major & Natural Minor (N.M.)':
        scales_data = df.iloc[0:7]
    elif chosen_geoscale == 'Harmonic Minor (H.M.)':
        scales_data = df.iloc[7:14]
    elif chosen_geoscale == 'Melodic Minor (M.M.)':
        scales_data = df.iloc[14:21]
        # Bebop
    elif chosen_geoscale == 'Bebop':
        scales_data = df.iloc[0:4]
    elif chosen_geoscale == 'Blues':
        scales_data = df.iloc[4:9]
    elif chosen_geoscale == 'Gypsy':
        scales_data = df.iloc[9:13]
    elif chosen_geoscale == 'Pentatonics':
        scales_data = df.iloc[13:18]
    elif chosen_geoscale == 'Whole-Half':
        scales_data = df.iloc[18:21]
    elif chosen_geoscale == 'Other':
        scales_data = df.iloc[21:34]
        # Other
    elif chosen_geoscale == 'Arabian':
        scales_data = df.iloc[0:13]
    elif chosen_geoscale == 'Chinese':
        scales_data = df.iloc[13:18]
    elif chosen_geoscale == 'Exotic':
        scales_data = df.iloc[18:22]
    elif chosen_geoscale == 'Greek':
        scales_data = df.iloc[22:37]
    elif chosen_geoscale == 'Indian':
        scales_data = df.iloc[37:61]
    elif chosen_geoscale == 'Indonesian':
        scales_data = df.iloc[61:66]
    elif chosen_geoscale == 'Japanese':
        scales_data = df.iloc[66:76]
    elif chosen_geoscale == 'Jewish':
        scales_data = df.iloc[76:79]

    return scales_data