import numpy as np
import SimpleITK as sitk
import torch

"""
The basis for the images and their usage in the code is the SimpleITK image.
The Dicom image read in by SimpleITK are always 3D, even the 2D images have a third dimension of 1
In order to prevent errors in the usage of 2D and 3D data, the slice index (3rd index) is the minimum between
image depth -1 and the chosen slice number 
"""

"""
transpose((1,2,0)) from sitk to numpy for the saggital view
transpose((2,0,1)) form numpy to sitk 
"""


class AbstractImage:
    def __init__(self, data=None, sequence_name="", folder_name="", slice_number=-1, shape=(1, 1, 1)):
        if data is None:
            self.data = sitk.Image(list(shape), sitk.sitkFloat32)
        else:
            self.data = data
        self.folder_name = folder_name
        self.sequence_name = sequence_name
        self.slice_number = slice_number

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, x):
        if isinstance(x, np.ndarray):
            sitk_image = self._data
            self._data = sitk.GetImageFromArray(x.transpose((2, 0, 1)), isVector=False)
            if x.shape == sitk_image.GetSize():
                self.CopyInformation(sitk_image)
        elif isinstance(x, sitk.Image):
            self._data = x
        else:
            raise ValueError("The setter function is implemented for numpy and sitk only")
        self.update_infos()

    @property
    def np_data(self, dtype="int16"):
        return sitk.GetArrayFromImage(self._data).astype(dtype).transpose((1, 2, 0))  # to saggital view

    @property
    def torch_data(self):
        return torch.from_numpy(self.np_data).permute(2, 1, 0)

    def __getitem__(self, *args, **kwargs):
        return self.np_data.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        np_temp = self.np_data.copy()
        np_temp.__setitem__(*args, **kwargs)
        self.data = np_temp

    @property
    def max(self):
        return self.np_data.max()

    @property
    def min(self):
        return self.np_data.min()

    @property
    def header(self):
        keys = self.GetMetaDataKeys()
        pixel_spacing = self.GetSpacing()
        header = dict(folder_name=self.folder_name,
                      slice_number=None,
                      sequence_name=self.sequence_name,
                      pixdim=[1.0] + list(pixel_spacing) + [.0, .0, .0, .0],
                      series_number=self.GetMetaData("0020|0011") if "0020|0011" in keys else None,
                      acquisition_date=self.GetMetaData("0008|0022") if "0008|0022" in keys else None,
                      patient_ID=self.GetMetaData("0010|0020") if "0010|0020" in keys else None,
                      patient_birthdate=self.GetMetaData("0010|0030") if "0010|0030" in keys else None,
                      patient_sex=self.GetMetaData("0010|0040") if "0010|0040" in keys else None,
                      patient_size=self.GetMetaData("0010|1020") if "0010|1020" in keys else None,
                      patient_weight=self.GetMetaData("0010|1030") if "0010|1030" in keys else None,
                      scl_slope=self.GetMetaData("0028|1053") if "0028|1053" in keys else None,
                      scl_inter=self.GetMetaData("0028|1052") if "0028|1052" in keys else None,
                      flip_angle=self.GetMetaData("0018|1314") if "0018|1314" in keys else None,
                      )
        return header

    def update_infos(self, folder_name=None, sequence_name=None):
        if folder_name is not None:
            self.folder_name = folder_name
        if sequence_name is not None:
            self.sequence_name = sequence_name

    def CopyInformation(self, sitk_image):
        for key in sitk_image.GetMetaDataKeys():
            self.SetMetaData(key, sitk_image.GetMetaData(key))
        self._data.CopyInformation(sitk_image)

    @property
    def spacing(self):
        return self.GetSpacing()

    def GetSpacing(self):
        return self._data.GetSpacing()

    @property
    def origin(self):
        return self.GetOrigin()

    def GetOrigin(self):
        return self._data.GetOrigin()

    @property
    def direction(self):
        return self.GetDirection()

    def GetDirection(self):
        return self._data.GetDirection()

    @property
    def shape(self):
        return self.GetSize()

    def GetSize(self):
        return self._data.GetSize()

    @property
    def depth(self):
        return self.GetDepth()

    def GetDepth(self):
        return self._data.GetDepth()

    @property
    def ndim(self):
        return self.GetDimension()

    def GetDimension(self):
        return self._data.GetDimension()

    def GetMetaDataKeys(self):
        return self._data.GetMetaDataKeys()

    def GetMetaData(self, key):
        return self._data.GetMetaData(key)

    def keys(self):
        return self.GetMetaDataKeys()

    def values(self):
        return [self.GetMetaData(k) for k in self.GetMetaDataKeys()]
        
    def items(self):
        return {k: self.GetMetaData(k) for k in self.GetMetaDataKeys()}

    def SetSpacing(self, spacing):
        self._data.SetSpacing(spacing)

    def SetOrigin(self, spacing):
        self._data.SetOrigin(spacing)

    def SetDirection(self, spacing):
        self._data.SetDirection(spacing)

    def SetMetaData(self, key, value):
        self._data.SetMetaData(key, value)
