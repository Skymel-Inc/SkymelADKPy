from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UniformRandomDistributionParameters(_message.Message):
    __slots__ = ("minimum_value", "maximum_value")
    MINIMUM_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_VALUE_FIELD_NUMBER: _ClassVar[int]
    minimum_value: float
    maximum_value: float
    def __init__(self, minimum_value: _Optional[float] = ..., maximum_value: _Optional[float] = ...) -> None: ...

class GaussianRandomDistributionParameters(_message.Message):
    __slots__ = ("mean", "standard_deviation")
    MEAN_FIELD_NUMBER: _ClassVar[int]
    STANDARD_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    mean: float
    standard_deviation: float
    def __init__(self, mean: _Optional[float] = ..., standard_deviation: _Optional[float] = ...) -> None: ...

class NumericValueGenerator(_message.Message):
    __slots__ = ("generator_type", "assigned_value", "uniform_random_distribution_parameters", "gaussian_random_distribution_parameters")
    class NumericValueGeneratorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_GENERATOR: _ClassVar[NumericValueGenerator.NumericValueGeneratorType]
        ASSIGNED_VALUE_REPEATS: _ClassVar[NumericValueGenerator.NumericValueGeneratorType]
        UNIFORM_RANDOM_DISTRIBUTION: _ClassVar[NumericValueGenerator.NumericValueGeneratorType]
        GAUSSIAN_RANDOM_DISTRIBUTION: _ClassVar[NumericValueGenerator.NumericValueGeneratorType]
    UNKNOWN_GENERATOR: NumericValueGenerator.NumericValueGeneratorType
    ASSIGNED_VALUE_REPEATS: NumericValueGenerator.NumericValueGeneratorType
    UNIFORM_RANDOM_DISTRIBUTION: NumericValueGenerator.NumericValueGeneratorType
    GAUSSIAN_RANDOM_DISTRIBUTION: NumericValueGenerator.NumericValueGeneratorType
    GENERATOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_RANDOM_DISTRIBUTION_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    GAUSSIAN_RANDOM_DISTRIBUTION_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    generator_type: NumericValueGenerator.NumericValueGeneratorType
    assigned_value: float
    uniform_random_distribution_parameters: UniformRandomDistributionParameters
    gaussian_random_distribution_parameters: GaussianRandomDistributionParameters
    def __init__(self, generator_type: _Optional[_Union[NumericValueGenerator.NumericValueGeneratorType, str]] = ..., assigned_value: _Optional[float] = ..., uniform_random_distribution_parameters: _Optional[_Union[UniformRandomDistributionParameters, _Mapping]] = ..., gaussian_random_distribution_parameters: _Optional[_Union[GaussianRandomDistributionParameters, _Mapping]] = ...) -> None: ...

class ArrayPaddingParameters(_message.Message):
    __slots__ = ("padding_generator", "padded_array_shape")
    PADDING_GENERATOR_FIELD_NUMBER: _ClassVar[int]
    PADDED_ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    padding_generator: NumericValueGenerator
    padded_array_shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, padding_generator: _Optional[_Union[NumericValueGenerator, _Mapping]] = ..., padded_array_shape: _Optional[_Iterable[int]] = ...) -> None: ...

class NodeOutputFloat(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape", "array_padding_parameters")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_PADDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: _containers.RepeatedScalarFieldContainer[float]
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    array_padding_parameters: ArrayPaddingParameters
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[_Iterable[float]] = ..., array_shape: _Optional[_Iterable[int]] = ..., array_padding_parameters: _Optional[_Union[ArrayPaddingParameters, _Mapping]] = ...) -> None: ...

class NodeOutputDouble(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape", "array_padding_parameters")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_PADDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: _containers.RepeatedScalarFieldContainer[float]
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    array_padding_parameters: ArrayPaddingParameters
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[_Iterable[float]] = ..., array_shape: _Optional[_Iterable[int]] = ..., array_padding_parameters: _Optional[_Union[ArrayPaddingParameters, _Mapping]] = ...) -> None: ...

class NodeOutputInt32(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape", "array_padding_parameters")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_PADDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: _containers.RepeatedScalarFieldContainer[int]
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    array_padding_parameters: ArrayPaddingParameters
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[_Iterable[int]] = ..., array_shape: _Optional[_Iterable[int]] = ..., array_padding_parameters: _Optional[_Union[ArrayPaddingParameters, _Mapping]] = ...) -> None: ...

class NodeOutputInt64(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape", "array_padding_parameters")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_PADDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: _containers.RepeatedScalarFieldContainer[int]
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    array_padding_parameters: ArrayPaddingParameters
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[_Iterable[int]] = ..., array_shape: _Optional[_Iterable[int]] = ..., array_padding_parameters: _Optional[_Union[ArrayPaddingParameters, _Mapping]] = ...) -> None: ...

class NodeOutputBytes(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: bytes
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[bytes] = ..., array_shape: _Optional[_Iterable[int]] = ...) -> None: ...

class NodeOutputString(_message.Message):
    __slots__ = ("node_name", "node_id", "output_strings")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_STRINGS_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_strings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_strings: _Optional[_Iterable[str]] = ...) -> None: ...

class NodeOutputBoolean(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: _containers.RepeatedScalarFieldContainer[bool]
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[_Iterable[bool]] = ..., array_shape: _Optional[_Iterable[int]] = ...) -> None: ...

class NodeOutputCompressedBytes(_message.Message):
    __slots__ = ("node_name", "node_id", "output_flat_array", "array_shape", "uncompressed_data_type", "compression_algorithm", "unlisted_algorithm_parameters", "zfp_parameters", "array_padding_parameters")
    class UncompressedDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_DATATYPE: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        BYTES: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        INT8: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        UINT8: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        INT16: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        UINT16: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        INT32: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        UINT32: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        INT64: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        UINT64: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        FLOAT16: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        FLOAT32: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        FLOAT64: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
        STRING: _ClassVar[NodeOutputCompressedBytes.UncompressedDataType]
    UNKNOWN_DATATYPE: NodeOutputCompressedBytes.UncompressedDataType
    BYTES: NodeOutputCompressedBytes.UncompressedDataType
    INT8: NodeOutputCompressedBytes.UncompressedDataType
    UINT8: NodeOutputCompressedBytes.UncompressedDataType
    INT16: NodeOutputCompressedBytes.UncompressedDataType
    UINT16: NodeOutputCompressedBytes.UncompressedDataType
    INT32: NodeOutputCompressedBytes.UncompressedDataType
    UINT32: NodeOutputCompressedBytes.UncompressedDataType
    INT64: NodeOutputCompressedBytes.UncompressedDataType
    UINT64: NodeOutputCompressedBytes.UncompressedDataType
    FLOAT16: NodeOutputCompressedBytes.UncompressedDataType
    FLOAT32: NodeOutputCompressedBytes.UncompressedDataType
    FLOAT64: NodeOutputCompressedBytes.UncompressedDataType
    STRING: NodeOutputCompressedBytes.UncompressedDataType
    class CompressionAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNLISTED_ALGORITHM: _ClassVar[NodeOutputCompressedBytes.CompressionAlgorithm]
        ZFP: _ClassVar[NodeOutputCompressedBytes.CompressionAlgorithm]
        FLOAT32_TO_FLOAT16_CONVERSION: _ClassVar[NodeOutputCompressedBytes.CompressionAlgorithm]
    UNLISTED_ALGORITHM: NodeOutputCompressedBytes.CompressionAlgorithm
    ZFP: NodeOutputCompressedBytes.CompressionAlgorithm
    FLOAT32_TO_FLOAT16_CONVERSION: NodeOutputCompressedBytes.CompressionAlgorithm
    class ZfpAlgorithmParameters(_message.Message):
        __slots__ = ("tolerance", "rate", "precision", "data_type", "nx", "ny", "nz", "nw", "uncompressed_data_size_bytes")
        class ZfpDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            ZFP_TYPE_NONE: _ClassVar[NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType]
            ZFP_TYPE_INT32: _ClassVar[NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType]
            ZFP_TYPE_INT64: _ClassVar[NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType]
            ZFP_TYPE_FLOAT: _ClassVar[NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType]
            ZFP_TYPE_DOUBLE: _ClassVar[NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType]
        ZFP_TYPE_NONE: NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType
        ZFP_TYPE_INT32: NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType
        ZFP_TYPE_INT64: NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType
        ZFP_TYPE_FLOAT: NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType
        ZFP_TYPE_DOUBLE: NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType
        TOLERANCE_FIELD_NUMBER: _ClassVar[int]
        RATE_FIELD_NUMBER: _ClassVar[int]
        PRECISION_FIELD_NUMBER: _ClassVar[int]
        DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
        NX_FIELD_NUMBER: _ClassVar[int]
        NY_FIELD_NUMBER: _ClassVar[int]
        NZ_FIELD_NUMBER: _ClassVar[int]
        NW_FIELD_NUMBER: _ClassVar[int]
        UNCOMPRESSED_DATA_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
        tolerance: float
        rate: float
        precision: int
        data_type: NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType
        nx: int
        ny: int
        nz: int
        nw: int
        uncompressed_data_size_bytes: int
        def __init__(self, tolerance: _Optional[float] = ..., rate: _Optional[float] = ..., precision: _Optional[int] = ..., data_type: _Optional[_Union[NodeOutputCompressedBytes.ZfpAlgorithmParameters.ZfpDataType, str]] = ..., nx: _Optional[int] = ..., ny: _Optional[int] = ..., nz: _Optional[int] = ..., nw: _Optional[int] = ..., uncompressed_data_size_bytes: _Optional[int] = ...) -> None: ...
    class UnlistedAlgorithmParameters(_message.Message):
        __slots__ = ("name", "additional_info")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
        name: str
        additional_info: bytes
        def __init__(self, name: _Optional[str] = ..., additional_info: _Optional[bytes] = ...) -> None: ...
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FLAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SHAPE_FIELD_NUMBER: _ClassVar[int]
    UNCOMPRESSED_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    UNLISTED_ALGORITHM_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ZFP_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ARRAY_PADDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    node_id: int
    output_flat_array: bytes
    array_shape: _containers.RepeatedScalarFieldContainer[int]
    uncompressed_data_type: NodeOutputCompressedBytes.UncompressedDataType
    compression_algorithm: NodeOutputCompressedBytes.CompressionAlgorithm
    unlisted_algorithm_parameters: NodeOutputCompressedBytes.UnlistedAlgorithmParameters
    zfp_parameters: NodeOutputCompressedBytes.ZfpAlgorithmParameters
    array_padding_parameters: ArrayPaddingParameters
    def __init__(self, node_name: _Optional[str] = ..., node_id: _Optional[int] = ..., output_flat_array: _Optional[bytes] = ..., array_shape: _Optional[_Iterable[int]] = ..., uncompressed_data_type: _Optional[_Union[NodeOutputCompressedBytes.UncompressedDataType, str]] = ..., compression_algorithm: _Optional[_Union[NodeOutputCompressedBytes.CompressionAlgorithm, str]] = ..., unlisted_algorithm_parameters: _Optional[_Union[NodeOutputCompressedBytes.UnlistedAlgorithmParameters, _Mapping]] = ..., zfp_parameters: _Optional[_Union[NodeOutputCompressedBytes.ZfpAlgorithmParameters, _Mapping]] = ..., array_padding_parameters: _Optional[_Union[ArrayPaddingParameters, _Mapping]] = ...) -> None: ...

class GraphOutput(_message.Message):
    __slots__ = ("float_outputs", "double_outputs", "int32_outputs", "int64_outputs", "bytes_outputs", "string_outputs", "compressed_bytes_outputs", "boolean_outputs")
    FLOAT_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    INT32_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    INT64_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    BYTES_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    STRING_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_BYTES_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    float_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputFloat]
    double_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputDouble]
    int32_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputInt32]
    int64_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputInt64]
    bytes_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputBytes]
    string_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputString]
    compressed_bytes_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputCompressedBytes]
    boolean_outputs: _containers.RepeatedCompositeFieldContainer[NodeOutputBoolean]
    def __init__(self, float_outputs: _Optional[_Iterable[_Union[NodeOutputFloat, _Mapping]]] = ..., double_outputs: _Optional[_Iterable[_Union[NodeOutputDouble, _Mapping]]] = ..., int32_outputs: _Optional[_Iterable[_Union[NodeOutputInt32, _Mapping]]] = ..., int64_outputs: _Optional[_Iterable[_Union[NodeOutputInt64, _Mapping]]] = ..., bytes_outputs: _Optional[_Iterable[_Union[NodeOutputBytes, _Mapping]]] = ..., string_outputs: _Optional[_Iterable[_Union[NodeOutputString, _Mapping]]] = ..., compressed_bytes_outputs: _Optional[_Iterable[_Union[NodeOutputCompressedBytes, _Mapping]]] = ..., boolean_outputs: _Optional[_Iterable[_Union[NodeOutputBoolean, _Mapping]]] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ("image_url", "image_bytes", "image_base64")
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BYTES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BASE64_FIELD_NUMBER: _ClassVar[int]
    image_url: str
    image_bytes: bytes
    image_base64: str
    def __init__(self, image_url: _Optional[str] = ..., image_bytes: _Optional[bytes] = ..., image_base64: _Optional[str] = ...) -> None: ...

class InferenceRequest(_message.Message):
    __slots__ = ("request_id", "api_key", "images", "texts", "token_ids", "graph_output")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    GRAPH_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    api_key: str
    images: _containers.RepeatedCompositeFieldContainer[Image]
    texts: _containers.RepeatedScalarFieldContainer[str]
    token_ids: _containers.RepeatedScalarFieldContainer[int]
    graph_output: _containers.RepeatedCompositeFieldContainer[GraphOutput]
    def __init__(self, request_id: _Optional[str] = ..., api_key: _Optional[str] = ..., images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ..., texts: _Optional[_Iterable[str]] = ..., token_ids: _Optional[_Iterable[int]] = ..., graph_output: _Optional[_Iterable[_Union[GraphOutput, _Mapping]]] = ...) -> None: ...

class ClassIdAndProbabilisticConfidenceScore(_message.Message):
    __slots__ = ("class_name", "class_id", "probabilistic_confidence")
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    PROBABILISTIC_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    class_id: int
    probabilistic_confidence: float
    def __init__(self, class_name: _Optional[str] = ..., class_id: _Optional[int] = ..., probabilistic_confidence: _Optional[float] = ...) -> None: ...

class ClassifierOutput(_message.Message):
    __slots__ = ("class_confidence_scores",)
    CLASS_CONFIDENCE_SCORES_FIELD_NUMBER: _ClassVar[int]
    class_confidence_scores: _containers.RepeatedCompositeFieldContainer[ClassIdAndProbabilisticConfidenceScore]
    def __init__(self, class_confidence_scores: _Optional[_Iterable[_Union[ClassIdAndProbabilisticConfidenceScore, _Mapping]]] = ...) -> None: ...

class StatusReport(_message.Message):
    __slots__ = ("status", "message")
    class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_STATUS: _ClassVar[StatusReport.StatusCode]
        SUCCESS: _ClassVar[StatusReport.StatusCode]
        CLIENT_ERROR: _ClassVar[StatusReport.StatusCode]
        SERVER_ERROR: _ClassVar[StatusReport.StatusCode]
        OTHER_ERROR: _ClassVar[StatusReport.StatusCode]
    UNKNOWN_STATUS: StatusReport.StatusCode
    SUCCESS: StatusReport.StatusCode
    CLIENT_ERROR: StatusReport.StatusCode
    SERVER_ERROR: StatusReport.StatusCode
    OTHER_ERROR: StatusReport.StatusCode
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: StatusReport.StatusCode
    message: str
    def __init__(self, status: _Optional[_Union[StatusReport.StatusCode, str]] = ..., message: _Optional[str] = ...) -> None: ...

class InferenceResponse(_message.Message):
    __slots__ = ("request_id", "status", "classifier_outputs", "text_outputs", "integer_outputs", "image_outputs", "graph_output")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CLASSIFIER_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    TEXT_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    INTEGER_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    GRAPH_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    status: StatusReport
    classifier_outputs: _containers.RepeatedCompositeFieldContainer[ClassifierOutput]
    text_outputs: _containers.RepeatedScalarFieldContainer[str]
    integer_outputs: _containers.RepeatedScalarFieldContainer[int]
    image_outputs: _containers.RepeatedCompositeFieldContainer[Image]
    graph_output: _containers.RepeatedCompositeFieldContainer[GraphOutput]
    def __init__(self, request_id: _Optional[str] = ..., status: _Optional[_Union[StatusReport, _Mapping]] = ..., classifier_outputs: _Optional[_Iterable[_Union[ClassifierOutput, _Mapping]]] = ..., text_outputs: _Optional[_Iterable[str]] = ..., integer_outputs: _Optional[_Iterable[int]] = ..., image_outputs: _Optional[_Iterable[_Union[Image, _Mapping]]] = ..., graph_output: _Optional[_Iterable[_Union[GraphOutput, _Mapping]]] = ...) -> None: ...

class ModelInputOutputDescription(_message.Message):
    __slots__ = ("name", "data_type", "data_shape")
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_TYPE: _ClassVar[ModelInputOutputDescription.DataType]
        BYTES: _ClassVar[ModelInputOutputDescription.DataType]
        UINT8: _ClassVar[ModelInputOutputDescription.DataType]
        INT32: _ClassVar[ModelInputOutputDescription.DataType]
        INT64: _ClassVar[ModelInputOutputDescription.DataType]
        FLOAT32: _ClassVar[ModelInputOutputDescription.DataType]
        DOUBLE: _ClassVar[ModelInputOutputDescription.DataType]
        LONG_DOUBLE: _ClassVar[ModelInputOutputDescription.DataType]
        STRING: _ClassVar[ModelInputOutputDescription.DataType]
    UNKNOWN_TYPE: ModelInputOutputDescription.DataType
    BYTES: ModelInputOutputDescription.DataType
    UINT8: ModelInputOutputDescription.DataType
    INT32: ModelInputOutputDescription.DataType
    INT64: ModelInputOutputDescription.DataType
    FLOAT32: ModelInputOutputDescription.DataType
    DOUBLE: ModelInputOutputDescription.DataType
    LONG_DOUBLE: ModelInputOutputDescription.DataType
    STRING: ModelInputOutputDescription.DataType
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_SHAPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    data_type: ModelInputOutputDescription.DataType
    data_shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[_Union[ModelInputOutputDescription.DataType, str]] = ..., data_shape: _Optional[_Iterable[int]] = ...) -> None: ...

class SensitiveDataSignature(_message.Message):
    __slots__ = ("signature", "public_key")
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    signature: str
    public_key: str
    def __init__(self, signature: _Optional[str] = ..., public_key: _Optional[str] = ...) -> None: ...

class ModelBinary(_message.Message):
    __slots__ = ("model_bytes", "is_compressed", "compression_algorithm", "signature")
    class CompressionAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_COMPRESSION: _ClassVar[ModelBinary.CompressionAlgorithm]
        GZIP: _ClassVar[ModelBinary.CompressionAlgorithm]
        BROTLI: _ClassVar[ModelBinary.CompressionAlgorithm]
        DEFLATE: _ClassVar[ModelBinary.CompressionAlgorithm]
    UNKNOWN_COMPRESSION: ModelBinary.CompressionAlgorithm
    GZIP: ModelBinary.CompressionAlgorithm
    BROTLI: ModelBinary.CompressionAlgorithm
    DEFLATE: ModelBinary.CompressionAlgorithm
    MODEL_BYTES_FIELD_NUMBER: _ClassVar[int]
    IS_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    model_bytes: bytes
    is_compressed: bool
    compression_algorithm: ModelBinary.CompressionAlgorithm
    signature: SensitiveDataSignature
    def __init__(self, model_bytes: _Optional[bytes] = ..., is_compressed: bool = ..., compression_algorithm: _Optional[_Union[ModelBinary.CompressionAlgorithm, str]] = ..., signature: _Optional[_Union[SensitiveDataSignature, _Mapping]] = ...) -> None: ...

class EndpointLocationAndId(_message.Message):
    __slots__ = ("endpoint_id", "endpoint_location", "endpoint_url")
    class EndpointLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_LOCATION: _ClassVar[EndpointLocationAndId.EndpointLocation]
        LOCAL: _ClassVar[EndpointLocationAndId.EndpointLocation]
        REMOTE: _ClassVar[EndpointLocationAndId.EndpointLocation]
    UNKNOWN_LOCATION: EndpointLocationAndId.EndpointLocation
    LOCAL: EndpointLocationAndId.EndpointLocation
    REMOTE: EndpointLocationAndId.EndpointLocation
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: str
    endpoint_location: EndpointLocationAndId.EndpointLocation
    endpoint_url: str
    def __init__(self, endpoint_id: _Optional[str] = ..., endpoint_location: _Optional[_Union[EndpointLocationAndId.EndpointLocation, str]] = ..., endpoint_url: _Optional[str] = ...) -> None: ...

class AbstractSyntaxTree(_message.Message):
    __slots__ = ("abstract_syntax_tree", "supported_languages")
    class SupportedLanguages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NO_KNOWN_LANGUAGE: _ClassVar[AbstractSyntaxTree.SupportedLanguages]
        JAVASCRIPT: _ClassVar[AbstractSyntaxTree.SupportedLanguages]
        PYTHON: _ClassVar[AbstractSyntaxTree.SupportedLanguages]
    NO_KNOWN_LANGUAGE: AbstractSyntaxTree.SupportedLanguages
    JAVASCRIPT: AbstractSyntaxTree.SupportedLanguages
    PYTHON: AbstractSyntaxTree.SupportedLanguages
    ABSTRACT_SYNTAX_TREE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    abstract_syntax_tree: bytes
    supported_languages: _containers.RepeatedScalarFieldContainer[AbstractSyntaxTree.SupportedLanguages]
    def __init__(self, abstract_syntax_tree: _Optional[bytes] = ..., supported_languages: _Optional[_Iterable[_Union[AbstractSyntaxTree.SupportedLanguages, str]]] = ...) -> None: ...

class InferenceEndpoint(_message.Message):
    __slots__ = ("endpoint_location_and_id", "model_runtime", "model_runtime_version", "model_inputs", "model_outputs", "model_binary", "model_runner", "chained_endpoint", "signature", "cache_preference")
    class ModelRuntime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_RUNTIME: _ClassVar[InferenceEndpoint.ModelRuntime]
        TF_LITE: _ClassVar[InferenceEndpoint.ModelRuntime]
        TF: _ClassVar[InferenceEndpoint.ModelRuntime]
        PYTORCH: _ClassVar[InferenceEndpoint.ModelRuntime]
        ONNX: _ClassVar[InferenceEndpoint.ModelRuntime]
    UNKNOWN_RUNTIME: InferenceEndpoint.ModelRuntime
    TF_LITE: InferenceEndpoint.ModelRuntime
    TF: InferenceEndpoint.ModelRuntime
    PYTORCH: InferenceEndpoint.ModelRuntime
    ONNX: InferenceEndpoint.ModelRuntime
    class LocalModelCachePreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT_PREFERENCE: _ClassVar[InferenceEndpoint.LocalModelCachePreference]
        INDEXED_DB: _ClassVar[InferenceEndpoint.LocalModelCachePreference]
        LOCAL_STORAGE: _ClassVar[InferenceEndpoint.LocalModelCachePreference]
        SESSION_STORAGE: _ClassVar[InferenceEndpoint.LocalModelCachePreference]
        NO_CACHING: _ClassVar[InferenceEndpoint.LocalModelCachePreference]
    DEFAULT_PREFERENCE: InferenceEndpoint.LocalModelCachePreference
    INDEXED_DB: InferenceEndpoint.LocalModelCachePreference
    LOCAL_STORAGE: InferenceEndpoint.LocalModelCachePreference
    SESSION_STORAGE: InferenceEndpoint.LocalModelCachePreference
    NO_CACHING: InferenceEndpoint.LocalModelCachePreference
    ENDPOINT_LOCATION_AND_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    MODEL_RUNTIME_VERSION_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_BINARY_FIELD_NUMBER: _ClassVar[int]
    MODEL_RUNNER_FIELD_NUMBER: _ClassVar[int]
    CHAINED_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    CACHE_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    endpoint_location_and_id: EndpointLocationAndId
    model_runtime: InferenceEndpoint.ModelRuntime
    model_runtime_version: str
    model_inputs: _containers.RepeatedCompositeFieldContainer[ModelInputOutputDescription]
    model_outputs: _containers.RepeatedCompositeFieldContainer[ModelInputOutputDescription]
    model_binary: ModelBinary
    model_runner: AbstractSyntaxTree
    chained_endpoint: EndpointLocationAndId
    signature: SensitiveDataSignature
    cache_preference: InferenceEndpoint.LocalModelCachePreference
    def __init__(self, endpoint_location_and_id: _Optional[_Union[EndpointLocationAndId, _Mapping]] = ..., model_runtime: _Optional[_Union[InferenceEndpoint.ModelRuntime, str]] = ..., model_runtime_version: _Optional[str] = ..., model_inputs: _Optional[_Iterable[_Union[ModelInputOutputDescription, _Mapping]]] = ..., model_outputs: _Optional[_Iterable[_Union[ModelInputOutputDescription, _Mapping]]] = ..., model_binary: _Optional[_Union[ModelBinary, _Mapping]] = ..., model_runner: _Optional[_Union[AbstractSyntaxTree, _Mapping]] = ..., chained_endpoint: _Optional[_Union[EndpointLocationAndId, _Mapping]] = ..., signature: _Optional[_Union[SensitiveDataSignature, _Mapping]] = ..., cache_preference: _Optional[_Union[InferenceEndpoint.LocalModelCachePreference, str]] = ...) -> None: ...

class ModelFetchRequest(_message.Message):
    __slots__ = ("api_key", "request_id", "endpoint_location_and_id")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_LOCATION_AND_ID_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    request_id: str
    endpoint_location_and_id: EndpointLocationAndId
    def __init__(self, api_key: _Optional[str] = ..., request_id: _Optional[str] = ..., endpoint_location_and_id: _Optional[_Union[EndpointLocationAndId, _Mapping]] = ...) -> None: ...

class ModelFetchResponse(_message.Message):
    __slots__ = ("request_id", "endpoint_location_and_id", "model_binary")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_LOCATION_AND_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_BINARY_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    endpoint_location_and_id: EndpointLocationAndId
    model_binary: ModelBinary
    def __init__(self, request_id: _Optional[str] = ..., endpoint_location_and_id: _Optional[_Union[EndpointLocationAndId, _Mapping]] = ..., model_binary: _Optional[_Union[ModelBinary, _Mapping]] = ...) -> None: ...

class TensorFlowJSModelArtifactsProto(_message.Message):
    __slots__ = ("converted_by", "format", "generated_by", "json_encoded_signature", "json_encoded_model_topology", "json_encoded_weight_specs", "json_encoded_training_config", "binary_weight_data", "name")
    CONVERTED_BY_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_FIELD_NUMBER: _ClassVar[int]
    JSON_ENCODED_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    JSON_ENCODED_MODEL_TOPOLOGY_FIELD_NUMBER: _ClassVar[int]
    JSON_ENCODED_WEIGHT_SPECS_FIELD_NUMBER: _ClassVar[int]
    JSON_ENCODED_TRAINING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BINARY_WEIGHT_DATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    converted_by: str
    format: str
    generated_by: str
    json_encoded_signature: str
    json_encoded_model_topology: str
    json_encoded_weight_specs: str
    json_encoded_training_config: str
    binary_weight_data: bytes
    name: str
    def __init__(self, converted_by: _Optional[str] = ..., format: _Optional[str] = ..., generated_by: _Optional[str] = ..., json_encoded_signature: _Optional[str] = ..., json_encoded_model_topology: _Optional[str] = ..., json_encoded_weight_specs: _Optional[str] = ..., json_encoded_training_config: _Optional[str] = ..., binary_weight_data: _Optional[bytes] = ..., name: _Optional[str] = ...) -> None: ...
