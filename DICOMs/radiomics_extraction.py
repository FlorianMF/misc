import os
from radiomics import featureextractor
import SimpleITK as sitk
import json

# Radiomics needs the images to be of the SimpleITK image type to extract features from the images
def calc_pyradiomics(image, segmentation, save_folder, sequence_name, whole_volume=True, slice_numbers=None):
    if whole_volume and slice_numbers:
        print("whole_volume cannot be True and slice_numbers defined at the same time")
        return ValueError

    if whole_volume:
        # Create the feature extractor
        extractor = featureextractor.RadiomicsFeaturesExtractor()

        # By default, only original is enabled. Optionally enable some image types:
        # extractor.enableImageTypes(Original={}, LoG={}, Wavelet={})
        extractor.enableAllImageTypes()

        # Disable all classes except firstorder
        # extractor.disableAllFeatures()

        # Enable all features in firstorder
        # extractor.enableFeatureClassByName('firstorder')

        # Only enable mean and skewness in firstorder
        # extractor.enableFeaturesByName(firstorder=['Mean', 'Skewness'])

        # extract the features
        result = extractor.execute(image, mask)
        
        # save the results to a csv and a json file
        filename = os.path.join(save_folder, sequence_name + "_whole_volume")
        os.makedirs(save_folder, exist_ok=True)
        # save as csv
        with open(filename + ".csv", "w") as f:  # context manager
            for key in result.keys():
                f.write(str(key).replace(";", ",") + ";")
            f.write("\n")
            for value in result.values():
                f.write(str(value).replace(";", ",") + ";")

        # save as json
        with open(filename + ".json", "w") as f:
            json.dump(result, f)
        
        return result

    else:
        # define the parameters you want to set for the feature extractor
        params={"force2D": True}
        # Create the feature extractor
        extractor = featureextractor.RadiomicsFeaturesExtractor(**params)
        extractor.enableAllImageTypes()

        # define a SimpleITK image slicer
        slicer = sitk.ExtractImageFilter()
        slicer.SetSize(list(image.GetSize()[:2])+[0])

        # extract the features from all image slices if not defined otherwise
        if not slice_numbers:
            slice_numbers = list(np.arange(image.GetDepth()))
        else:
            assert type(slice_numbers) == list

        filename = os.path.join(save_folder, sequence_name + "_per_slice")
        os.makedirs(save_folder, exist_ok=True)

        # create a list to save the features of each slice
        result_list = []

        for slice_nr in slice_numbers:
            # slice the image
            image_slice = np.expand_dims(sitk.GetArrayFromImage(image[:, :, slice_nr]) * 1000, -1)
            image_slice = sitk.GetImageFromArray(image_slice, isVector=False)
            image_slice.SetSpacing(image.GetSpacing())

            # slice the segmentation
            segm_slice = np.expand_dims(sitk.GetArrayFromImage(segmentation[:, :, slice_nr]), -1)
            segm_slice = sitk.GetImageFromArray(segm_slice, isVector=False)
            
            # we assume that the image and segmentation have the same geometric information
            segm_slice.CopyInformation(image_slice)  

            # extract the features
            result = extractor.execute(image_slice, segm_slice)
            
            # add the key Slice_Nr at the beginning of the OrderedDict result
            result.update({'Slice_Nr': slice_nr+1})
            result.move_to_end('Slice_Nr', last=False)
            result_list.append(result)

            # save as csv
            with open(filename + ".csv", "w") as f:
                for key in result_list[0].keys():
                    f.write(str(key).replace(";", ",") + ";")
                f.write("\n")
                for result in result_list:
                    for value in result.values():
                        f.write(str(value).replace(";", ",") + ";")
                    f.write("\n")

            # save as json
            with open(filename + ".json", "w", encoding="utf-8") as f:
                json.dump(result_list, f)

        return result_list


if __name__ == "__main__":
    import numpy as np

    sequence_name = "seq1"
    save_folder = "/path/to/saving/folder"

    whole_volume = False
    slice_numbers = [1, 3, 6]
    image_size = (64, 64)
    
    image = sitk.Image(image_size[0], image_size][1], sitk.sitkFloat32)
    segmentation = sitk.GetImageFromArray(np.random.randint(0, 2, image_size)

    features = calc_pyradiomics(image, segmentation, save_folder, sequence_name,
                                 whole_volume, slice_numbers)
