# -*- coding: utf-8 -*-

from typing import Dict, Tuple, Union
import numpy as np
from PySide2.QtGui import QDoubleValidator, QIntValidator, QValidator

from .common.structure import *

ValidatorUInt8 = QIntValidator(np.iinfo(np.uint8).min, np.iinfo(np.uint8).max)
ValidatorInt8 = QIntValidator(np.iinfo(np.int8).min, np.iinfo(np.int8).max)
ValidatorUInt16 = QIntValidator(np.iinfo(np.uint16).min, np.iinfo(np.uint16).max)
ValidatorInt16 = QIntValidator(np.iinfo(np.int16).min, np.iinfo(np.int16).max)
ValidatorPInt32 = QIntValidator(0, np.iinfo(np.int32).max)
ValidatorInt32 = QIntValidator(np.iinfo(np.int32).min, np.iinfo(np.int32).max)
ValidatorUFloat = QDoubleValidator(0.0, np.inf, 1000)
ValidatorFloat = QDoubleValidator(-np.inf, np.inf, 1000)

SHAPE_TYPES:Dict[str, Union[Tuple[Union[int, QValidator, None], ...], None]] = {
    TYPE_FLOAT16: None,
    TYPE_FLOAT32: None,
    TYPE_FLOAT64: None,
    TYPE_UINT8: None,
    TYPE_INT8: None,
    TYPE_INT16: None,
    TYPE_INT32: None,
    TYPE_INT64: None,
    TYPE_MONO8: (ValidatorPInt32, ValidatorPInt32),
    TYPE_MONO16: (ValidatorPInt32, ValidatorPInt32),
    TYPE_BGR8: (ValidatorPInt32, ValidatorPInt32, 3),
    TYPE_RGB8: (ValidatorPInt32, ValidatorPInt32, 3),
    TYPE_BGRA8: (ValidatorPInt32, ValidatorPInt32, 4),
    TYPE_RGBA8: (ValidatorPInt32, ValidatorPInt32, 4),
    TYPE_DEPTH: (ValidatorPInt32, ValidatorPInt32),
    TYPE_POINTS: (None, 3),
    TYPE_VOXEL_POINTS: None,
    TYPE_SEMANTIC1D: (None,),
    TYPE_SEMANTIC2D: (ValidatorPInt32, ValidatorPInt32),
    TYPE_SEMANTIC3D: (None,),
    TYPE_VOXEL_SEMANTIC3D: None,
    TYPE_POSE: None,
    TYPE_TRANSLATION: (3,),
    TYPE_QUATERNION: (4,),
    TYPE_INTRINSIC: None,
    TYPE_COLOR: (3,),
}

SHAPE_PLACEHOLDER:Dict[str, Union[Tuple[str], None]] = {
    TYPE_FLOAT16: None,
    TYPE_FLOAT32: None,
    TYPE_FLOAT64: None,
    TYPE_UINT8: None,
    TYPE_INT8: None,
    TYPE_INT16: None,
    TYPE_INT32: None,
    TYPE_INT64: None,
    TYPE_MONO8: ('Height [px]', 'Width [px]'),
    TYPE_MONO16: ('Height [px]', 'Width [px]'),
    TYPE_BGR8: ('Height [px]', 'Width [px]', None),
    TYPE_RGB8: ('Height [px]', 'Width [px]', None),
    TYPE_BGRA8: ('Height [px]', 'Width [px]', None),
    TYPE_RGBA8: ('Height [px]', 'Width [px]', None),
    TYPE_DEPTH: ('Height [px]', 'Width [px]'),
    TYPE_POINTS: (None, None),
    TYPE_VOXEL_POINTS: None,
    TYPE_SEMANTIC1D: (None,),
    TYPE_SEMANTIC2D: ('Height [px]', 'Width [px]'),
    TYPE_SEMANTIC3D: (None,),
    TYPE_VOXEL_SEMANTIC3D: None,
    TYPE_POSE: None,
    TYPE_TRANSLATION: (None,),
    TYPE_QUATERNION: (None,),
    TYPE_INTRINSIC: None,
    TYPE_COLOR: (None,),
}

RANGE_VALIDATOR:Dict[str, Union[QValidator, None]] = {
    TYPE_FLOAT16: ValidatorFloat,
    TYPE_FLOAT32: ValidatorFloat,
    TYPE_FLOAT64: ValidatorFloat,
    TYPE_UINT8: ValidatorUInt8,
    TYPE_INT8: ValidatorInt8,
    TYPE_INT16: ValidatorInt16,
    TYPE_INT32: ValidatorInt32,
    TYPE_INT64: ValidatorInt32,
    TYPE_MONO8: ValidatorUInt8,
    TYPE_MONO16: ValidatorUInt16,
    TYPE_BGR8: ValidatorUInt8,
    TYPE_RGB8: ValidatorUInt8,
    TYPE_BGRA8: ValidatorUInt8,
    TYPE_RGBA8: ValidatorUInt8,
    TYPE_DEPTH: ValidatorUFloat,
    TYPE_POINTS: ValidatorFloat,
    TYPE_VOXEL_POINTS: None,
    TYPE_SEMANTIC1D: None,
    TYPE_SEMANTIC2D: None,
    TYPE_SEMANTIC3D: ValidatorFloat,
    TYPE_VOXEL_SEMANTIC3D: None,
    TYPE_POSE: None,
    TYPE_TRANSLATION: None,
    TYPE_QUATERNION: None,
    TYPE_INTRINSIC: None,
    TYPE_COLOR: ValidatorUInt8,
}
