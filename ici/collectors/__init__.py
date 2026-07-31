"""Collector abstractions and registry exports."""

from .base import BaseCollector
from .company_financials.collector import CompanyFinancialsCollector
from .company_intelligence import CompanyIntelligenceCollector
from .company_master import CompanyMasterCollector
from .company_ranking import CompanyRankingCollector
from .investment_decision import InvestmentDecisionCollector
from .registry import CollectorRegistry, get_registry

__all__ = [
    "BaseCollector",
    "CompanyMasterCollector",
    "CompanyFinancialsCollector",
    "CompanyIntelligenceCollector",
    "CompanyRankingCollector",
    "InvestmentDecisionCollector",
    "CollectorRegistry",
    "get_registry",
]