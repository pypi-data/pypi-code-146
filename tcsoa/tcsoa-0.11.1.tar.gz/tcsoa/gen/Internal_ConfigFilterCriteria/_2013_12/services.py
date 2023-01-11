from __future__ import annotations

from tcsoa.gen.Internal.ConfigFilterCriteria._2013_12.VariantManagement import ConfiguratorServiceResponse
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def executeConfiguratorService(cls, inputXMLString: str, configuratorURL: str) -> ConfiguratorServiceResponse:
        """
        This service implements a mechanism to process the following configurator services:
        CheckOverlap
        ConvertExpressionToString
        ConvertStringToExpression
        GetPersistentID
        GetProductVariability
        GetTrueAvailability
        GetValidFeatureCombinations
        ValidateFeatureExpression
        ValidateAndCompleteFeatureCombination
        Consumers of this service need to provide an XML string as input and will receive an XML string as output. The
        input and output XML strings will be as per the XML schema definitions located in DMS at
        "//plm/tcpmm10.1.1/tcbom/configurator/xids".
        These XML schema definitions follow standard Teamcenter versioning procedure.
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException wrapping around the following Teamcenter
        errors:
        
        92001    An internal error has occurred in the "Fnd0SoaConfigFilterCriteria" module.
        92002    The Product Name and Product Namespace must not be empty.
        256000    An internal configurator error occurred.
        256001    A general configurator error occurred.
        256002    The following product is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256003    The following feature value is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256004    The following feature family is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256005    An invalid feature combination was found (Context: info).
        256006    An invalid product configuration was found (Context: info).
        256007    An invalid expression was found (Context: info).
        256008    The following Boolean operator is invalid: opcode (Context: info).
        256009    An invalid effectivity date was found (Context: info).
        256010    A time-out occurred (Context: info).
        256011    A resource is not available (Context: info).
        256012    The following functionality is not implemented: function (Version: TcVersion).
        256013    A configurator implementation specific error occurred (Context: info).
        256014    The variant expression contains unmatched quote at position number.
        256015    The variant expression contains unmatched bracket at position number.
        256016    An unexpected token 'text' was found at position number.
        256017    The entry 'text' was found at position number when an option value was expected.
        256018    The token 'text' is missing after 'text' at position number.
        256019    The variant expression adaptor does not support text used at position number.
        256020    The XML tag 'text' has no text value.
        256021    The string 'formula' cannot be converted into an expression. 
        256022    The operator code 'opcode' in token at position number is unknown.
        256023    The variant value 'text' in token at position number is unknown.
        256024    The variant family 'text' in token at position number is unknown.
        256025    An ambiguous option value name 'FamilyName' in namespace 'DictionaryNamespace' in token at position
        number was found: text.
        256026    An ambiguous option family name 'FamilyName' in token at position number was found: 'text'.
        256027    The option namespace 'DictionaryNamespace' in token at position number is invalid.
        256028    The variant family 'FamilyName' in token at position number is invalid.
        256029    The variant option value 'text' for family 'FamilyName' in token at position number is invalid.
        256030    The variant option value 'text' for family 'FamilyName' in token at position number is invalid: its
        value is not numeric.
        256031    The variant option value 'text' for family 'FamilyName' in token at position number is invalid: the
        value unit of measure 'text' does not match the family unit of measure 'text'.
        256032    The option / family / family namespace combination 'text' / 'FamilyName' / 'DictionaryNamespace' in
        token at position number is invalid.
        256033    The family 'FamilyName' for option / family namespace combination 'text' / 'DictionaryNamespace' in
        token at position number is invalid. 
        256034    There is no option value in token at position number.
        256035    The variant option value 'text' for family 'FamilyName' in token at position 'number' is invalid: the
        value is not a valid date.
        """
        return cls.execute_soa_method(
            method_name='executeConfiguratorService',
            library='Internal-ConfigFilterCriteria',
            service_date='2013_12',
            service_name='VariantManagement',
            params={'inputXMLString': inputXMLString, 'configuratorURL': configuratorURL},
            response_cls=ConfiguratorServiceResponse,
        )
