import uuid
from typing import Optional

from pydantic import BaseModel

from telescope_sdk.common import IngestedDataType, Location, Source
from telescope_sdk.company_types import CompanyType, PDLCompanyType
from telescope_sdk.utils import convert_pdl_company_type_to_company_type, get_current_datetime_aws_format


class CompanySizeRange(BaseModel):
    lower: Optional[int]
    upper: Optional[int]


class Company(IngestedDataType):
    name: str
    linkedin_internal_id: str
    linkedin_url: str
    pdl_id: Optional[str] = None
    universal_name_id: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    domain_name: Optional[str] = None
    website: Optional[str] = None
    landing_page_content: Optional[str] = None
    logo_url: Optional[str] = None
    embeddings: Optional[list[float]] = None
    industry: Optional[str] = None
    categories: Optional[list[str]] = None
    specialties: Optional[list[str]] = None
    company_type: Optional[CompanyType] = None
    company_size_range: Optional[CompanySizeRange] = None
    company_size_on_linkedin: Optional[int] = None
    founded_year: Optional[int] = None
    hq: Optional[Location] = None
    locations: Optional[list[Location]] = None
    last_enriched_at: Optional[str] = None

    @staticmethod
    def from_pdl(pdl_input: dict[str, any]) -> Optional['Company']:
        name = pdl_input.get('name')
        linkedin_internal_id = pdl_input.get('linkedin_id')
        if not name or not linkedin_internal_id:
            return None

        pdl_domain_name = pdl_input.get('website')
        pdl_company_type = pdl_input.get('type')
        pdl_company_size = pdl_input.get('size')
        pdl_company_size_range_split = pdl_company_size.split('-') if pdl_company_size else None
        pdl_location = pdl_input.get('location')

        return Company(
            id=str(uuid.uuid4()),
            source=Source.PDL,
            version=0,
            created_at=get_current_datetime_aws_format(),
            updated_at=get_current_datetime_aws_format(),
            name=name,
            linkedin_internal_id=linkedin_internal_id,
            pdl_id=pdl_input.get('id'),
            universal_name_id=pdl_input.get('id'),
            tagline=pdl_input.get('headline'),
            description=pdl_input.get('summary'),
            domain_name=pdl_domain_name,
            website=f'https://{pdl_domain_name}' if pdl_domain_name else None,
            linkedin_url=pdl_input.get('linkedin_url') or f'https://www.linkedin.com/company/{linkedin_internal_id}',
            industry=pdl_input.get('industry'),  # should this be canonical?
            categories=pdl_input.get('tags'),
            company_type=CompanyType(convert_pdl_company_type_to_company_type(PDLCompanyType[pdl_company_type]))
            if pdl_company_type else None,
            company_size_range=CompanySizeRange(
                lower=int(pdl_company_size_range_split[0]),
                upper=int(pdl_company_size_range_split[1])
            ) if pdl_company_size_range_split and len(pdl_company_size_range_split) == 2 else None,
            company_size_on_linkedin=pdl_input.get('employee_count'),
            founded_year=pdl_input.get('founded'),
            hq=Location.from_pdl(pdl_location) if pdl_location else None,
            locations=[Location.from_pdl(pdl_location)] if pdl_location else None,
            last_enriched_at=get_current_datetime_aws_format()
        )
