"""
SEEKER Global Analytics Validation System
Comprehensive global market intelligence and supplier analysis platform
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class Continent(Enum):
    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    ASIA = "asia"
    SOUTH_AMERICA = "south_america"
    AFRICA = "africa"
    AUSTRALIA_OCEANIA = "australia_oceania"
    ANTARCTICA = "antarctica"

class DataSource(Enum):
    MANUFACTURER_DB = "manufacturer_database"
    INDUSTRY_ASSOCIATION = "industry_association"
    GOVERNMENT_TRADE = "government_trade"
    BUSINESS_DIRECTORY = "business_directory"
    PRICING_FEED = "pricing_feed"

@dataclass
class MarketData:
    continent: Continent
    country: str
    industry: str
    supplier_name: str
    product_category: str
    price_usd: float
    quality_score: float
    reliability_score: float
    lead_time_days: int
    compliance_status: str
    last_updated: datetime
    data_source: DataSource

@dataclass
class AnalyticsResult:
    market_penetration: float
    competitive_landscape: Dict[str, Any]
    price_quality_matrix: Dict[str, float]
    supply_chain_routes: List[Dict[str, Any]]
    compliance_status: Dict[str, bool]
    opportunity_score: float

class SEEKERGlobalAnalyticsService:
    """
    Global Analytics Validation System for comprehensive market intelligence
    """
    
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.db = mongo_client.seeker_global_analytics
        self.collections = {
            'market_data': self.db.market_data,
            'analytics_results': self.db.analytics_results,
            'supplier_profiles': self.db.supplier_profiles,
            'pricing_history': self.db.pricing_history
        }
        
        # Data collection APIs configuration
        self.data_sources = {
            Continent.NORTH_AMERICA: {
                'manufacturer_db': 'https://api.manufacturers-na.com/v1',
                'trade_api': 'https://api.trade.gov/v1',
                'industry_association': 'https://api.naics.org/v1'
            },
            Continent.EUROPE: {
                'eu_trade_data': 'https://api.eurostat.europa.eu/v1',
                'national_registries': 'https://api.european-business.org/v1',
                'industry_association': 'https://api.cefic.org/v1'
            },
            Continent.ASIA: {
                'manufacturing_hubs': 'https://api.asia-manufacturing.org/v1',
                'supplier_networks': 'https://api.asia-suppliers.com/v1',
                'trade_data': 'https://api.asia-trade.org/v1'
            },
            Continent.SOUTH_AMERICA: {
                'regional_trade': 'https://api.mercosur.org/v1',
                'business_directory': 'https://api.south-america-business.org/v1',
                'trade_partnerships': 'https://api.south-america-trade.org/v1'
            },
            Continent.AFRICA: {
                'emerging_markets': 'https://api.africa-markets.org/v1',
                'business_directory': 'https://api.africa-business.org/v1',
                'trade_data': 'https://api.africa-trade.org/v1'
            },
            Continent.AUSTRALIA_OCEANIA: {
                'resource_sector': 'https://api.australia-resources.org/v1',
                'business_directory': 'https://api.australia-business.org/v1',
                'trade_data': 'https://api.australia-trade.org/v1'
            },
            Continent.ANTARCTICA: {
                'research_equipment': 'https://api.antarctica-research.org/v1',
                'specialized_suppliers': 'https://api.antarctica-suppliers.org/v1'
            }
        }
        
        logger.info("🌍 SEEKER Global Analytics Service initialized")
    
    async def collect_global_market_data(self, industry: str, product_category: str) -> List[MarketData]:
        """
        Collect market data from all continents for specified industry and product category
        """
        logger.info(f"📊 Collecting global market data for {industry} - {product_category}")
        
        all_market_data = []
        
        # Collect data from all continents concurrently
        tasks = []
        for continent in Continent:
            task = self._collect_continental_data(continent, industry, product_category)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_market_data.extend(result)
            else:
                logger.error(f"Error collecting data: {result}")
        
        # Store in database
        if all_market_data:
            await self._store_market_data(all_market_data)
        
        logger.info(f"✅ Collected {len(all_market_data)} market data points globally")
        return all_market_data
    
    async def _collect_continental_data(self, continent: Continent, industry: str, product_category: str) -> List[MarketData]:
        """
        Collect market data from specific continent
        """
        logger.info(f"🌍 Collecting data from {continent.value}")
        
        market_data = []
        
        try:
            # Simulate API calls to various data sources
            async with aiohttp.ClientSession() as session:
                # Manufacturer database
                manufacturer_data = await self._fetch_manufacturer_data(session, continent, industry, product_category)
                market_data.extend(manufacturer_data)
                
                # Industry association data
                association_data = await self._fetch_association_data(session, continent, industry, product_category)
                market_data.extend(association_data)
                
                # Government trade data
                trade_data = await self._fetch_trade_data(session, continent, industry, product_category)
                market_data.extend(trade_data)
                
                # Business directory data
                directory_data = await self._fetch_directory_data(session, continent, industry, product_category)
                market_data.extend(directory_data)
                
                # Real-time pricing feeds
                pricing_data = await self._fetch_pricing_data(session, continent, industry, product_category)
                market_data.extend(pricing_data)
                
        except Exception as e:
            logger.error(f"Error collecting data from {continent.value}: {e}")
        
        return market_data
    
    async def _fetch_manufacturer_data(self, session: aiohttp.ClientSession, continent: Continent, industry: str, product_category: str) -> List[MarketData]:
        """Fetch manufacturer database data"""
        # Simulate API call
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Generate sample manufacturer data
        manufacturers = [
            MarketData(
                continent=continent,
                country=self._get_sample_country(continent),
                industry=industry,
                supplier_name=f"{continent.value.title()} {industry} Manufacturer {i}",
                product_category=product_category,
                price_usd=round(np.random.uniform(100, 10000), 2),
                quality_score=round(np.random.uniform(0.6, 0.95), 2),
                reliability_score=round(np.random.uniform(0.7, 0.98), 2),
                lead_time_days=np.random.randint(5, 60),
                compliance_status="COMPLIANT" if np.random.random() > 0.2 else "PENDING",
                last_updated=datetime.now(),
                data_source=DataSource.MANUFACTURER_DB
            )
            for i in range(np.random.randint(3, 8))
        ]
        
        return manufacturers
    
    async def _fetch_association_data(self, session: aiohttp.ClientSession, continent: Continent, industry: str, product_category: str) -> List[MarketData]:
        """Fetch industry association data"""
        await asyncio.sleep(0.1)
        
        associations = [
            MarketData(
                continent=continent,
                country=self._get_sample_country(continent),
                industry=industry,
                supplier_name=f"{continent.value.title()} {industry} Association Member {i}",
                product_category=product_category,
                price_usd=round(np.random.uniform(150, 12000), 2),
                quality_score=round(np.random.uniform(0.7, 0.96), 2),
                reliability_score=round(np.random.uniform(0.75, 0.99), 2),
                lead_time_days=np.random.randint(3, 45),
                compliance_status="COMPLIANT",
                last_updated=datetime.now(),
                data_source=DataSource.INDUSTRY_ASSOCIATION
            )
            for i in range(np.random.randint(2, 6))
        ]
        
        return associations
    
    async def _fetch_trade_data(self, session: aiohttp.ClientSession, continent: Continent, industry: str, product_category: str) -> List[MarketData]:
        """Fetch government trade data"""
        await asyncio.sleep(0.1)
        
        trade_suppliers = [
            MarketData(
                continent=continent,
                country=self._get_sample_country(continent),
                industry=industry,
                supplier_name=f"{continent.value.title()} Trade Partner {i}",
                product_category=product_category,
                price_usd=round(np.random.uniform(80, 8000), 2),
                quality_score=round(np.random.uniform(0.5, 0.9), 2),
                reliability_score=round(np.random.uniform(0.6, 0.95), 2),
                lead_time_days=np.random.randint(7, 90),
                compliance_status="COMPLIANT" if np.random.random() > 0.3 else "UNDER_REVIEW",
                last_updated=datetime.now(),
                data_source=DataSource.GOVERNMENT_TRADE
            )
            for i in range(np.random.randint(2, 5))
        ]
        
        return trade_suppliers
    
    async def _fetch_directory_data(self, session: aiohttp.ClientSession, continent: Continent, industry: str, product_category: str) -> List[MarketData]:
        """Fetch business directory data"""
        await asyncio.sleep(0.1)
        
        directory_suppliers = [
            MarketData(
                continent=continent,
                country=self._get_sample_country(continent),
                industry=industry,
                supplier_name=f"{continent.value.title()} Directory Supplier {i}",
                product_category=product_category,
                price_usd=round(np.random.uniform(120, 9000), 2),
                quality_score=round(np.random.uniform(0.4, 0.85), 2),
                reliability_score=round(np.random.uniform(0.5, 0.9), 2),
                lead_time_days=np.random.randint(10, 75),
                compliance_status="COMPLIANT" if np.random.random() > 0.4 else "PENDING",
                last_updated=datetime.now(),
                data_source=DataSource.BUSINESS_DIRECTORY
            )
            for i in range(np.random.randint(3, 7))
        ]
        
        return directory_suppliers
    
    async def _fetch_pricing_data(self, session: aiohttp.ClientSession, continent: Continent, industry: str, product_category: str) -> List[MarketData]:
        """Fetch real-time pricing data"""
        await asyncio.sleep(0.1)
        
        pricing_suppliers = [
            MarketData(
                continent=continent,
                country=self._get_sample_country(continent),
                industry=industry,
                supplier_name=f"{continent.value.title()} Market Supplier {i}",
                product_category=product_category,
                price_usd=round(np.random.uniform(90, 11000), 2),
                quality_score=round(np.random.uniform(0.6, 0.92), 2),
                reliability_score=round(np.random.uniform(0.65, 0.97), 2),
                lead_time_days=np.random.randint(5, 60),
                compliance_status="COMPLIANT" if np.random.random() > 0.25 else "PENDING",
                last_updated=datetime.now(),
                data_source=DataSource.PRICING_FEED
            )
            for i in range(np.random.randint(2, 6))
        ]
        
        return pricing_suppliers
    
    def _get_sample_country(self, continent: Continent) -> str:
        """Get sample country for continent"""
        countries = {
            Continent.NORTH_AMERICA: ["USA", "Canada", "Mexico"],
            Continent.EUROPE: ["Germany", "France", "UK", "Italy", "Spain"],
            Continent.ASIA: ["China", "Japan", "South Korea", "India", "Singapore"],
            Continent.SOUTH_AMERICA: ["Brazil", "Argentina", "Chile", "Colombia"],
            Continent.AFRICA: ["South Africa", "Nigeria", "Kenya", "Egypt"],
            Continent.AUSTRALIA_OCEANIA: ["Australia", "New Zealand", "Fiji"],
            Continent.ANTARCTICA: ["Research Station Alpha", "Research Station Beta"]
        }
        
        return np.random.choice(countries[continent])
    
    async def _store_market_data(self, market_data: List[MarketData]):
        """Store market data in MongoDB"""
        documents = []
        for data in market_data:
            doc = {
                'continent': data.continent.value,
                'country': data.country,
                'industry': data.industry,
                'supplier_name': data.supplier_name,
                'product_category': data.product_category,
                'price_usd': data.price_usd,
                'quality_score': data.quality_score,
                'reliability_score': data.reliability_score,
                'lead_time_days': data.lead_time_days,
                'compliance_status': data.compliance_status,
                'last_updated': data.last_updated,
                'data_source': data.data_source.value
            }
            documents.append(doc)
        
        if documents:
            await self.collections['market_data'].insert_many(documents)
    
    async def analyze_global_market(self, industry: str, product_category: str) -> AnalyticsResult:
        """
        Perform comprehensive global market analysis
        """
        logger.info(f"🔍 Analyzing global market for {industry} - {product_category}")
        
        # Collect fresh market data
        market_data = await self.collect_global_market_data(industry, product_category)
        
        if not market_data:
            raise HTTPException(status_code=404, detail="No market data available for analysis")
        
        # Perform analysis
        market_penetration = self._calculate_market_penetration(market_data)
        competitive_landscape = self._analyze_competitive_landscape(market_data)
        price_quality_matrix = self._create_price_quality_matrix(market_data)
        supply_chain_routes = self._analyze_supply_chain_routes(market_data)
        compliance_status = self._check_compliance_status(market_data)
        opportunity_score = self._calculate_opportunity_score(market_data)
        
        result = AnalyticsResult(
            market_penetration=market_penetration,
            competitive_landscape=competitive_landscape,
            price_quality_matrix=price_quality_matrix,
            supply_chain_routes=supply_chain_routes,
            compliance_status=compliance_status,
            opportunity_score=opportunity_score
        )
        
        # Store analysis result
        await self._store_analytics_result(result, industry, product_category)
        
        logger.info(f"✅ Global market analysis completed for {industry} - {product_category}")
        return result
    
    def _calculate_market_penetration(self, market_data: List[MarketData]) -> float:
        """Calculate market penetration score"""
        total_suppliers = len(market_data)
        continents_covered = len(set(data.continent for data in market_data))
        max_continents = len(Continent)
        
        # Weighted score based on supplier density and continental coverage
        supplier_density = min(total_suppliers / 50, 1.0)  # Normalize to 50 suppliers
        continental_coverage = continents_covered / max_continents
        
        return round((supplier_density * 0.6 + continental_coverage * 0.4) * 100, 2)
    
    def _analyze_competitive_landscape(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze competitive landscape"""
        # Group by continent
        continent_data = {}
        for data in market_data:
            if data.continent.value not in continent_data:
                continent_data[data.continent.value] = []
            continent_data[data.continent.value].append(data)
        
        # Calculate competitive metrics per continent
        competitive_metrics = {}
        for continent, data_list in continent_data.items():
            prices = [d.price_usd for d in data_list]
            quality_scores = [d.quality_score for d in data_list]
            reliability_scores = [d.reliability_score for d in data_list]
            
            competitive_metrics[continent] = {
                'supplier_count': len(data_list),
                'avg_price': round(np.mean(prices), 2),
                'price_range': {'min': round(min(prices), 2), 'max': round(max(prices), 2)},
                'avg_quality': round(np.mean(quality_scores), 2),
                'avg_reliability': round(np.mean(reliability_scores), 2),
                'price_volatility': round(np.std(prices), 2)
            }
        
        return competitive_metrics
    
    def _create_price_quality_matrix(self, market_data: List[MarketData]) -> Dict[str, float]:
        """Create price-quality optimization matrix"""
        # Calculate price-quality efficiency scores
        efficiency_scores = {}
        
        for data in market_data:
            # Efficiency = Quality Score / (Price / 1000) - normalized price
            efficiency = data.quality_score / (data.price_usd / 1000)
            efficiency_scores[data.supplier_name] = round(efficiency, 3)
        
        # Get top performers
        sorted_suppliers = sorted(efficiency_scores.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_suppliers[:10])  # Top 10 suppliers
    
    def _analyze_supply_chain_routes(self, market_data: List[MarketData]) -> List[Dict[str, Any]]:
        """Analyze supply chain routes and optimization"""
        routes = []
        
        # Group by continent and analyze routes
        continent_groups = {}
        for data in market_data:
            if data.continent.value not in continent_groups:
                continent_groups[data.continent.value] = []
            continent_groups[data.continent.value].append(data)
        
        for continent, suppliers in continent_groups.items():
            avg_lead_time = np.mean([s.lead_time_days for s in suppliers])
            avg_reliability = np.mean([s.reliability_score for s in suppliers])
            total_cost = sum([s.price_usd for s in suppliers])
            
            routes.append({
                'continent': continent,
                'supplier_count': len(suppliers),
                'avg_lead_time_days': round(avg_lead_time, 1),
                'avg_reliability': round(avg_reliability, 3),
                'total_cost_usd': round(total_cost, 2),
                'route_efficiency': round(avg_reliability / (avg_lead_time / 30), 3)  # Monthly efficiency
            })
        
        return routes
    
    def _check_compliance_status(self, market_data: List[MarketData]) -> Dict[str, bool]:
        """Check compliance status across regions"""
        compliance_status = {}
        
        # Check compliance by continent
        for continent in Continent:
            continent_data = [d for d in market_data if d.continent == continent]
            if continent_data:
                compliant_count = sum(1 for d in continent_data if d.compliance_status == "COMPLIANT")
                compliance_rate = compliant_count / len(continent_data)
                compliance_status[continent.value] = compliance_rate > 0.8  # 80% threshold
        
        return compliance_status
    
    def _calculate_opportunity_score(self, market_data: List[MarketData]) -> float:
        """Calculate overall market opportunity score"""
        if not market_data:
            return 0.0
        
        # Factors: supplier diversity, price competitiveness, quality, reliability
        supplier_diversity = len(set(d.supplier_name for d in market_data)) / 20  # Normalize to 20 suppliers
        avg_price = np.mean([d.price_usd for d in market_data])
        price_competitiveness = max(0, 1 - (avg_price / 5000))  # Lower price = higher score
        avg_quality = np.mean([d.quality_score for d in market_data])
        avg_reliability = np.mean([d.reliability_score for d in market_data])
        
        # Weighted opportunity score
        opportunity_score = (
            supplier_diversity * 0.25 +
            price_competitiveness * 0.25 +
            avg_quality * 0.25 +
            avg_reliability * 0.25
        )
        
        return round(opportunity_score * 100, 2)
    
    async def _store_analytics_result(self, result: AnalyticsResult, industry: str, product_category: str):
        """Store analytics result in database"""
        doc = {
            'industry': industry,
            'product_category': product_category,
            'analysis_timestamp': datetime.now(),
            'market_penetration': result.market_penetration,
            'competitive_landscape': result.competitive_landscape,
            'price_quality_matrix': result.price_quality_matrix,
            'supply_chain_routes': result.supply_chain_routes,
            'compliance_status': result.compliance_status,
            'opportunity_score': result.opportunity_score
        }
        
        await self.collections['analytics_results'].insert_one(doc)
    
    async def get_global_heatmap_data(self, industry: str, product_category: str) -> Dict[str, Any]:
        """Get data for global heatmap visualization"""
        # Get latest analytics result
        result = await self.collections['analytics_results'].find_one(
            {'industry': industry, 'product_category': product_category},
            sort=[('analysis_timestamp', -1)]
        )
        
        if not result:
            # Perform fresh analysis
            analytics_result = await self.analyze_global_market(industry, product_category)
            result = {
                'competitive_landscape': analytics_result.competitive_landscape,
                'opportunity_score': analytics_result.opportunity_score,
                'market_penetration': analytics_result.market_penetration
            }
        
        return {
            'heatmap_data': result['competitive_landscape'],
            'opportunity_score': result['opportunity_score'],
            'market_penetration': result['market_penetration'],
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_supplier_reliability_scores(self, industry: str, product_category: str) -> List[Dict[str, Any]]:
        """Get supplier reliability scores for visualization"""
        # Get market data
        market_data = await self.collections['market_data'].find({
            'industry': industry,
            'product_category': product_category
        }).sort('last_updated', -1).limit(100).to_list(length=100)
        
        suppliers = []
        for data in market_data:
            suppliers.append({
                'supplier_name': data['supplier_name'],
                'continent': data['continent'],
                'country': data['country'],
                'reliability_score': data['reliability_score'],
                'quality_score': data['quality_score'],
                'price_usd': data['price_usd'],
                'lead_time_days': data['lead_time_days']
            })
        
        return suppliers 

    async def get_advanced_market_insights(self, industry: str, product_category: str) -> Dict[str, Any]:
        """
        Get advanced market insights with detailed competitive analysis
        """
        logger.info(f"🔍 Generating advanced market insights for {industry} - {product_category}")
        
        # Collect comprehensive market data
        market_data = await self.collect_global_market_data(industry, product_category)
        
        if not market_data:
            raise HTTPException(status_code=404, detail="No market data available for analysis")
        
        # Advanced analysis
        insights = {
            'market_overview': self._generate_market_overview(market_data),
            'competitive_analysis': self._perform_competitive_analysis(market_data),
            'supply_chain_optimization': self._analyze_supply_chain_optimization(market_data),
            'risk_assessment': self._assess_market_risks(market_data),
            'opportunity_mapping': self._map_market_opportunities(market_data),
            'trend_analysis': self._analyze_market_trends(market_data),
            'regional_insights': self._generate_regional_insights(market_data)
        }
        
        return insights
    
    def _generate_market_overview(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Generate comprehensive market overview"""
        total_suppliers = len(market_data)
        continents_covered = len(set(data.continent for data in market_data))
        
        # Price analysis
        prices = [data.price_usd for data in market_data]
        avg_price = np.mean(prices)
        price_std = np.std(prices)
        price_range = {'min': min(prices), 'max': max(prices), 'median': np.median(prices)}
        
        # Quality analysis
        quality_scores = [data.quality_score for data in market_data]
        avg_quality = np.mean(quality_scores)
        quality_distribution = {
            'excellent': len([q for q in quality_scores if q >= 0.9]),
            'good': len([q for q in quality_scores if 0.8 <= q < 0.9]),
            'average': len([q for q in quality_scores if 0.7 <= q < 0.8]),
            'below_average': len([q for q in quality_scores if q < 0.7])
        }
        
        # Reliability analysis
        reliability_scores = [data.reliability_score for data in market_data]
        avg_reliability = np.mean(reliability_scores)
        
        return {
            'total_suppliers': total_suppliers,
            'continents_covered': continents_covered,
            'geographic_coverage': f"{continents_covered}/7 continents",
            'price_analysis': {
                'average_price': round(avg_price, 2),
                'price_volatility': round(price_std, 2),
                'price_range': price_range,
                'price_efficiency': round(avg_quality / (avg_price / 1000), 3)
            },
            'quality_analysis': {
                'average_quality': round(avg_quality, 3),
                'quality_distribution': quality_distribution,
                'quality_percentile': {
                    'top_10%': round(np.percentile(quality_scores, 90), 3),
                    'top_25%': round(np.percentile(quality_scores, 75), 3),
                    'median': round(np.percentile(quality_scores, 50), 3)
                }
            },
            'reliability_analysis': {
                'average_reliability': round(avg_reliability, 3),
                'reliability_percentile': {
                    'top_10%': round(np.percentile(reliability_scores, 90), 3),
                    'top_25%': round(np.percentile(reliability_scores, 75), 3)
                }
            }
        }
    
    def _perform_competitive_analysis(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Perform detailed competitive analysis"""
        # Group by continent for regional competition
        continent_groups = {}
        for data in market_data:
            if data.continent.value not in continent_groups:
                continent_groups[data.continent.value] = []
            continent_groups[data.continent.value].append(data)
        
        competitive_metrics = {}
        for continent, suppliers in continent_groups.items():
            prices = [s.price_usd for s in suppliers]
            qualities = [s.quality_score for s in suppliers]
            reliabilities = [s.reliability_score for s in suppliers]
            
            # Competitive intensity
            price_competition = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0
            quality_competition = np.std(qualities) / np.mean(qualities) if np.mean(qualities) > 0 else 0
            
            # Market concentration
            market_concentration = len(suppliers) / len(market_data) if len(market_data) > 0 else 0
            
            competitive_metrics[continent] = {
                'supplier_count': len(suppliers),
                'market_share': round(market_concentration * 100, 2),
                'price_competition_index': round(price_competition, 3),
                'quality_competition_index': round(quality_competition, 3),
                'average_price': round(np.mean(prices), 2),
                'average_quality': round(np.mean(qualities), 3),
                'average_reliability': round(np.mean(reliabilities), 3),
                'competitive_intensity': round((price_competition + quality_competition) / 2, 3)
            }
        
        # Overall competitive landscape
        all_prices = [data.price_usd for data in market_data]
        all_qualities = [data.quality_score for data in market_data]
        
        return {
            'regional_competition': competitive_metrics,
            'overall_competitive_landscape': {
                'total_competitors': len(market_data),
                'price_competition_level': 'High' if np.std(all_prices) / np.mean(all_prices) > 0.3 else 'Medium' if np.std(all_prices) / np.mean(all_prices) > 0.15 else 'Low',
                'quality_competition_level': 'High' if np.std(all_qualities) > 0.1 else 'Medium' if np.std(all_qualities) > 0.05 else 'Low',
                'market_fragmentation': 'High' if len(market_data) > 50 else 'Medium' if len(market_data) > 20 else 'Low'
            }
        }
    
    def _analyze_supply_chain_optimization(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze supply chain optimization opportunities"""
        # Lead time analysis
        lead_times = [data.lead_time_days for data in market_data]
        avg_lead_time = np.mean(lead_times)
        
        # Cost-quality optimization
        cost_quality_ratios = [(data.quality_score / (data.price_usd / 1000)) for data in market_data]
        optimal_suppliers = sorted(zip(market_data, cost_quality_ratios), key=lambda x: x[1], reverse=True)[:10]
        
        # Regional supply chain analysis
        regional_supply_chains = {}
        for continent in Continent:
            continent_data = [d for d in market_data if d.continent == continent]
            if continent_data:
                avg_lead_time_regional = np.mean([d.lead_time_days for d in continent_data])
                avg_reliability_regional = np.mean([d.reliability_score for d in continent_data])
                avg_cost_regional = np.mean([d.price_usd for d in continent_data])
                
                regional_supply_chains[continent.value] = {
                    'supplier_count': len(continent_data),
                    'average_lead_time': round(avg_lead_time_regional, 1),
                    'average_reliability': round(avg_reliability_regional, 3),
                    'average_cost': round(avg_cost_regional, 2),
                    'supply_chain_efficiency': round(avg_reliability_regional / (avg_lead_time_regional / 30), 3)
                }
        
        return {
            'overall_supply_chain': {
                'average_lead_time_days': round(avg_lead_time, 1),
                'lead_time_percentiles': {
                    'fastest_10%': round(np.percentile(lead_times, 10), 1),
                    'fastest_25%': round(np.percentile(lead_times, 25), 1),
                    'median': round(np.percentile(lead_times, 50), 1)
                }
            },
            'optimal_suppliers': [
                {
                    'supplier_name': supplier.supplier_name,
                    'continent': supplier.continent.value,
                    'cost_quality_ratio': round(ratio, 3),
                    'price': supplier.price_usd,
                    'quality': supplier.quality_score,
                    'reliability': supplier.reliability_score
                }
                for supplier, ratio in optimal_suppliers
            ],
            'regional_supply_chains': regional_supply_chains,
            'optimization_recommendations': self._generate_supply_chain_recommendations(market_data)
        }
    
    def _generate_supply_chain_recommendations(self, market_data: List[MarketData]) -> List[Dict[str, Any]]:
        """Generate supply chain optimization recommendations"""
        recommendations = []
        
        # Price optimization
        prices = [data.price_usd for data in market_data]
        if len(prices) > 0:
            price_median = np.median(prices)
            low_cost_suppliers = [data for data in market_data if data.price_usd < price_median * 0.8]
            if low_cost_suppliers:
                recommendations.append({
                    'type': 'cost_optimization',
                    'title': 'Cost Reduction Opportunity',
                    'description': f'Found {len(low_cost_suppliers)} suppliers with prices 20% below median',
                    'potential_savings': f'Up to {round((price_median - min(prices)) / price_median * 100, 1)}% cost reduction',
                    'priority': 'High'
                })
        
        # Quality improvement
        high_quality_suppliers = [data for data in market_data if data.quality_score >= 0.9]
        if high_quality_suppliers:
            recommendations.append({
                'type': 'quality_improvement',
                'title': 'Premium Quality Suppliers',
                'description': f'Identified {len(high_quality_suppliers)} suppliers with 90%+ quality scores',
                'benefit': 'Enhanced product quality and customer satisfaction',
                'priority': 'Medium'
            })
        
        # Lead time optimization
        fast_suppliers = [data for data in market_data if data.lead_time_days <= 10]
        if fast_suppliers:
            recommendations.append({
                'type': 'speed_optimization',
                'title': 'Fast Delivery Suppliers',
                'description': f'Found {len(fast_suppliers)} suppliers with 10-day or faster lead times',
                'benefit': 'Reduced inventory costs and faster time-to-market',
                'priority': 'High'
            })
        
        return recommendations
    
    def _assess_market_risks(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Assess market risks and vulnerabilities"""
        risks = {
            'supply_concentration_risk': self._assess_supply_concentration_risk(market_data),
            'geographic_risk': self._assess_geographic_risk(market_data),
            'quality_risk': self._assess_quality_risk(market_data),
            'compliance_risk': self._assess_compliance_risk(market_data),
            'price_volatility_risk': self._assess_price_volatility_risk(market_data)
        }
        
        # Overall risk score
        risk_scores = [risk['score'] for risk in risks.values()]
        overall_risk_score = np.mean(risk_scores) if risk_scores else 0
        
        return {
            'risk_assessment': risks,
            'overall_risk_score': round(overall_risk_score, 2),
            'risk_level': 'High' if overall_risk_score > 0.7 else 'Medium' if overall_risk_score > 0.4 else 'Low',
            'risk_mitigation_strategies': self._generate_risk_mitigation_strategies(risks)
        }
    
    def _assess_supply_concentration_risk(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Assess risk from supply concentration"""
        total_suppliers = len(market_data)
        if total_suppliers == 0:
            return {'score': 1.0, 'level': 'Critical', 'description': 'No suppliers available'}
        
        # Check for single supplier dominance
        supplier_counts = {}
        for data in market_data:
            supplier_counts[data.continent.value] = supplier_counts.get(data.continent.value, 0) + 1
        
        max_concentration = max(supplier_counts.values()) / total_suppliers if total_suppliers > 0 else 0
        
        if max_concentration > 0.5:
            score = 0.9
            level = 'High'
            description = f'High concentration risk: {round(max_concentration * 100, 1)}% of suppliers in single region'
        elif max_concentration > 0.3:
            score = 0.6
            level = 'Medium'
            description = f'Moderate concentration risk: {round(max_concentration * 100, 1)}% of suppliers in single region'
        else:
            score = 0.2
            level = 'Low'
            description = 'Well-distributed supplier base across regions'
        
        return {'score': score, 'level': level, 'description': description}
    
    def _assess_geographic_risk(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Assess geographic risk factors"""
        continents_covered = len(set(data.continent for data in market_data))
        
        if continents_covered <= 2:
            score = 0.8
            level = 'High'
            description = f'Limited geographic coverage: only {continents_covered} continents'
        elif continents_covered <= 4:
            score = 0.5
            level = 'Medium'
            description = f'Moderate geographic coverage: {continents_covered} continents'
        else:
            score = 0.2
            level = 'Low'
            description = f'Good geographic diversification: {continents_covered} continents'
        
        return {'score': score, 'level': level, 'description': description}
    
    def _assess_quality_risk(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Assess quality-related risks"""
        if not market_data:
            return {'score': 1.0, 'level': 'Critical', 'description': 'No quality data available'}
        
        quality_scores = [data.quality_score for data in market_data]
        avg_quality = np.mean(quality_scores)
        low_quality_count = len([q for q in quality_scores if q < 0.7])
        
        if avg_quality < 0.7 or low_quality_count > len(quality_scores) * 0.3:
            score = 0.8
            level = 'High'
            description = f'Quality risk: {low_quality_count} suppliers with quality scores below 70%'
        elif avg_quality < 0.8:
            score = 0.5
            level = 'Medium'
            description = f'Moderate quality risk: average quality score {round(avg_quality * 100, 1)}%'
        else:
            score = 0.2
            level = 'Low'
            description = f'Good quality standards: average quality score {round(avg_quality * 100, 1)}%'
        
        return {'score': score, 'level': level, 'description': description}
    
    def _assess_compliance_risk(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Assess compliance risk"""
        if not market_data:
            return {'score': 1.0, 'level': 'Critical', 'description': 'No compliance data available'}
        
        compliant_count = len([data for data in market_data if data.compliance_status == "COMPLIANT"])
        compliance_rate = compliant_count / len(market_data)
        
        if compliance_rate < 0.7:
            score = 0.9
            level = 'High'
            description = f'High compliance risk: only {round(compliance_rate * 100, 1)}% of suppliers are compliant'
        elif compliance_rate < 0.9:
            score = 0.6
            level = 'Medium'
            description = f'Moderate compliance risk: {round(compliance_rate * 100, 1)}% of suppliers are compliant'
        else:
            score = 0.1
            level = 'Low'
            description = f'Good compliance: {round(compliance_rate * 100, 1)}% of suppliers are compliant'
        
        return {'score': score, 'level': level, 'description': description}
    
    def _assess_price_volatility_risk(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Assess price volatility risk"""
        if not market_data:
            return {'score': 1.0, 'level': 'Critical', 'description': 'No price data available'}
        
        prices = [data.price_usd for data in market_data]
        price_cv = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0
        
        if price_cv > 0.5:
            score = 0.8
            level = 'High'
            description = f'High price volatility: coefficient of variation {round(price_cv, 2)}'
        elif price_cv > 0.3:
            score = 0.5
            level = 'Medium'
            description = f'Moderate price volatility: coefficient of variation {round(price_cv, 2)}'
        else:
            score = 0.2
            level = 'Low'
            description = f'Stable pricing: coefficient of variation {round(price_cv, 2)}'
        
        return {'score': score, 'level': level, 'description': description}
    
    def _generate_risk_mitigation_strategies(self, risks: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        for risk_type, risk_data in risks.items():
            if risk_data['level'] in ['High', 'Critical']:
                if risk_type == 'supply_concentration_risk':
                    strategies.append({
                        'risk_type': 'Supply Concentration',
                        'strategy': 'Diversify supplier base across multiple regions',
                        'priority': 'High',
                        'expected_impact': 'Reduce single-point-of-failure risk'
                    })
                elif risk_type == 'geographic_risk':
                    strategies.append({
                        'risk_type': 'Geographic Risk',
                        'strategy': 'Expand supplier network to additional continents',
                        'priority': 'High',
                        'expected_impact': 'Improve geographic diversification'
                    })
                elif risk_type == 'quality_risk':
                    strategies.append({
                        'risk_type': 'Quality Risk',
                        'strategy': 'Implement quality assurance programs and supplier audits',
                        'priority': 'High',
                        'expected_impact': 'Improve product quality and reduce defects'
                    })
                elif risk_type == 'compliance_risk':
                    strategies.append({
                        'risk_type': 'Compliance Risk',
                        'strategy': 'Establish compliance monitoring and supplier certification programs',
                        'priority': 'High',
                        'expected_impact': 'Ensure regulatory compliance and reduce legal risks'
                    })
                elif risk_type == 'price_volatility_risk':
                    strategies.append({
                        'risk_type': 'Price Volatility',
                        'strategy': 'Implement long-term contracts and price hedging strategies',
                        'priority': 'Medium',
                        'expected_impact': 'Stabilize costs and improve budget predictability'
                    })
        
        return strategies
    
    def _map_market_opportunities(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Map market opportunities and growth potential"""
        opportunities = {
            'cost_optimization': self._identify_cost_optimization_opportunities(market_data),
            'quality_improvement': self._identify_quality_improvement_opportunities(market_data),
            'geographic_expansion': self._identify_geographic_expansion_opportunities(market_data),
            'supplier_development': self._identify_supplier_development_opportunities(market_data)
        }
        
        return opportunities
    
    def _identify_cost_optimization_opportunities(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Identify cost optimization opportunities"""
        if not market_data:
            return {'opportunities': [], 'potential_savings': 0}
        
        prices = [data.price_usd for data in market_data]
        median_price = np.median(prices)
        
        # Find suppliers with better cost-quality ratios
        cost_quality_ratios = [(data.quality_score / (data.price_usd / 1000)) for data in market_data]
        best_ratios = sorted(zip(market_data, cost_quality_ratios), key=lambda x: x[1], reverse=True)[:5]
        
        opportunities = []
        for supplier, ratio in best_ratios:
            if supplier.price_usd < median_price:
                savings_potential = (median_price - supplier.price_usd) / median_price * 100
                opportunities.append({
                    'supplier_name': supplier.supplier_name,
                    'continent': supplier.continent.value,
                    'current_price': supplier.price_usd,
                    'quality_score': supplier.quality_score,
                    'cost_quality_ratio': round(ratio, 3),
                    'potential_savings': round(savings_potential, 1)
                })
        
        total_potential_savings = sum(opp['potential_savings'] for opp in opportunities)
        
        return {
            'opportunities': opportunities,
            'potential_savings': round(total_potential_savings, 1),
            'recommendation': f'Focus on {len(opportunities)} suppliers with superior cost-quality ratios'
        }
    
    def _identify_quality_improvement_opportunities(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Identify quality improvement opportunities"""
        if not market_data:
            return {'opportunities': [], 'quality_gap': 0}
        
        quality_scores = [data.quality_score for data in market_data]
        avg_quality = np.mean(quality_scores)
        
        # Find high-quality suppliers
        high_quality_suppliers = [data for data in market_data if data.quality_score >= 0.9]
        
        opportunities = []
        for supplier in high_quality_suppliers[:5]:  # Top 5
            quality_gap = (supplier.quality_score - avg_quality) / avg_quality * 100
            opportunities.append({
                'supplier_name': supplier.supplier_name,
                'continent': supplier.continent.value,
                'quality_score': supplier.quality_score,
                'price': supplier.price_usd,
                'quality_gap': round(quality_gap, 1),
                'recommendation': 'Premium quality supplier for high-end applications'
            })
        
        return {
            'opportunities': opportunities,
            'quality_gap': round((max(quality_scores) - avg_quality) / avg_quality * 100, 1),
            'recommendation': f'Consider {len(opportunities)} premium suppliers for quality-critical applications'
        }
    
    def _identify_geographic_expansion_opportunities(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Identify geographic expansion opportunities"""
        continent_coverage = set(data.continent for data in market_data)
        all_continents = set(Continent)
        uncovered_continents = all_continents - continent_coverage
        
        opportunities = []
        for continent in uncovered_continents:
            opportunities.append({
                'continent': continent.value,
                'opportunity_type': 'Market Entry',
                'description': f'Expand supplier network to {continent.value.replace("_", " ").title()}',
                'potential_benefits': ['Geographic diversification', 'New market access', 'Risk reduction'],
                'priority': 'High' if continent in [Continent.ASIA, Continent.EUROPE] else 'Medium'
            })
        
        return {
            'opportunities': opportunities,
            'coverage_gap': len(uncovered_continents),
            'recommendation': f'Expand to {len(uncovered_continents)} uncovered continents for better diversification'
        }
    
    def _identify_supplier_development_opportunities(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Identify supplier development opportunities"""
        if not market_data:
            return {'opportunities': [], 'development_potential': 0}
        
        # Find suppliers with potential for improvement
        improvement_candidates = []
        for data in market_data:
            improvement_score = 0
            improvements = []
            
            if data.quality_score < 0.8:
                improvement_score += 1
                improvements.append('Quality improvement')
            
            if data.reliability_score < 0.8:
                improvement_score += 1
                improvements.append('Reliability improvement')
            
            if data.lead_time_days > 30:
                improvement_score += 1
                improvements.append('Lead time reduction')
            
            if improvement_score > 0:
                improvement_candidates.append({
                    'supplier_name': data.supplier_name,
                    'continent': data.continent.value,
                    'improvement_areas': improvements,
                    'improvement_score': improvement_score,
                    'current_metrics': {
                        'quality': data.quality_score,
                        'reliability': data.reliability_score,
                        'lead_time': data.lead_time_days
                    }
                })
        
        # Sort by improvement potential
        improvement_candidates.sort(key=lambda x: x['improvement_score'], reverse=True)
        
        return {
            'opportunities': improvement_candidates[:10],  # Top 10
            'development_potential': len(improvement_candidates),
            'recommendation': f'Focus on developing {len(improvement_candidates[:5])} suppliers with highest improvement potential'
        }
    
    def _analyze_market_trends(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze market trends and patterns"""
        if not market_data:
            return {'trends': [], 'insights': []}
        
        # Price trends by continent
        continent_price_trends = {}
        for continent in Continent:
            continent_data = [data for data in market_data if data.continent == continent]
            if continent_data:
                prices = [data.price_usd for data in continent_data]
                continent_price_trends[continent.value] = {
                    'average_price': round(np.mean(prices), 2),
                    'price_range': {'min': round(min(prices), 2), 'max': round(max(prices), 2)},
                    'price_volatility': round(np.std(prices), 2),
                    'supplier_count': len(continent_data)
                }
        
        # Quality trends
        quality_trends = {
            'overall_average': round(np.mean([data.quality_score for data in market_data]), 3),
            'by_continent': {}
        }
        
        for continent in Continent:
            continent_data = [data for data in market_data if data.continent == continent]
            if continent_data:
                qualities = [data.quality_score for data in continent_data]
                quality_trends['by_continent'][continent.value] = round(np.mean(qualities), 3)
        
        # Market maturity analysis
        supplier_counts = {}
        for data in market_data:
            supplier_counts[data.continent.value] = supplier_counts.get(data.continent.value, 0) + 1
        
        market_maturity = {}
        for continent, count in supplier_counts.items():
            if count > 10:
                maturity = 'Mature'
            elif count > 5:
                maturity = 'Developing'
            else:
                maturity = 'Emerging'
            
            market_maturity[continent] = {
                'supplier_count': count,
                'maturity_level': maturity,
                'growth_potential': 'High' if maturity == 'Emerging' else 'Medium' if maturity == 'Developing' else 'Low'
            }
        
        return {
            'price_trends': continent_price_trends,
            'quality_trends': quality_trends,
            'market_maturity': market_maturity,
            'key_insights': self._generate_market_insights(market_data)
        }
    
    def _generate_market_insights(self, market_data: List[MarketData]) -> List[str]:
        """Generate key market insights"""
        insights = []
        
        if not market_data:
            return ['No market data available for analysis']
        
        # Price insights
        prices = [data.price_usd for data in market_data]
        price_cv = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0
        
        if price_cv > 0.4:
            insights.append(f'High price variability ({round(price_cv * 100, 1)}% CV) suggests opportunity for cost optimization')
        else:
            insights.append('Stable pricing environment indicates mature, competitive market')
        
        # Quality insights
        quality_scores = [data.quality_score for data in market_data]
        avg_quality = np.mean(quality_scores)
        
        if avg_quality > 0.85:
            insights.append('High average quality standards across the market')
        elif avg_quality < 0.75:
            insights.append('Quality improvement opportunities exist in the market')
        
        # Geographic insights
        continent_coverage = len(set(data.continent for data in market_data))
        
        if continent_coverage >= 5:
            insights.append('Good geographic diversification reduces supply chain risks')
        else:
            insights.append(f'Limited to {continent_coverage} continents - consider geographic expansion')
        
        # Supplier concentration insights
        supplier_counts = {}
        for data in market_data:
            supplier_counts[data.continent.value] = supplier_counts.get(data.continent.value, 0) + 1
        
        max_concentration = max(supplier_counts.values()) / len(market_data) if market_data else 0
        
        if max_concentration > 0.4:
            insights.append('High supplier concentration in single region - diversification recommended')
        
        return insights
    
    def _generate_regional_insights(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Generate detailed regional market insights"""
        regional_insights = {}
        
        for continent in Continent:
            continent_data = [data for data in market_data if data.continent == continent]
            if continent_data:
                prices = [data.price_usd for data in continent_data]
                qualities = [data.quality_score for data in continent_data]
                reliabilities = [data.reliability_score for data in continent_data]
                lead_times = [data.lead_time_days for data in continent_data]
                
                regional_insights[continent.value] = {
                    'market_overview': {
                        'supplier_count': len(continent_data),
                        'average_price': round(np.mean(prices), 2),
                        'average_quality': round(np.mean(qualities), 3),
                        'average_reliability': round(np.mean(reliabilities), 3),
                        'average_lead_time': round(np.mean(lead_times), 1)
                    },
                    'competitive_landscape': {
                        'price_competition': 'High' if np.std(prices) / np.mean(prices) > 0.3 else 'Medium' if np.std(prices) / np.mean(prices) > 0.15 else 'Low',
                        'quality_competition': 'High' if np.std(qualities) > 0.1 else 'Medium' if np.std(qualities) > 0.05 else 'Low',
                        'market_maturity': 'Mature' if len(continent_data) > 10 else 'Developing' if len(continent_data) > 5 else 'Emerging'
                    },
                    'strengths': self._identify_regional_strengths(continent_data),
                    'opportunities': self._identify_regional_opportunities(continent_data),
                    'risks': self._identify_regional_risks(continent_data)
                }
        
        return regional_insights
    
    def _identify_regional_strengths(self, continent_data: List[MarketData]) -> List[str]:
        """Identify regional market strengths"""
        strengths = []
        
        if not continent_data:
            return strengths
        
        prices = [data.price_usd for data in continent_data]
        qualities = [data.quality_score for data in continent_data]
        reliabilities = [data.reliability_score for data in continent_data]
        lead_times = [data.lead_time_days for data in continent_data]
        
        # Price strengths
        if np.mean(prices) < np.median(prices):
            strengths.append('Competitive pricing compared to global average')
        
        # Quality strengths
        if np.mean(qualities) > 0.85:
            strengths.append('High quality standards')
        elif np.mean(qualities) > 0.8:
            strengths.append('Good quality performance')
        
        # Reliability strengths
        if np.mean(reliabilities) > 0.9:
            strengths.append('Excellent supplier reliability')
        elif np.mean(reliabilities) > 0.8:
            strengths.append('Good supplier reliability')
        
        # Lead time strengths
        if np.mean(lead_times) < 15:
            strengths.append('Fast delivery times')
        elif np.mean(lead_times) < 30:
            strengths.append('Reasonable lead times')
        
        return strengths
    
    def _identify_regional_opportunities(self, continent_data: List[MarketData]) -> List[str]:
        """Identify regional market opportunities"""
        opportunities = []
        
        if not continent_data:
            return opportunities
        
        prices = [data.price_usd for data in continent_data]
        qualities = [data.quality_score for data in continent_data]
        reliabilities = [data.reliability_score for data in continent_data]
        lead_times = [data.lead_time_days for data in continent_data]
        
        # Price opportunities
        if np.std(prices) / np.mean(prices) > 0.3:
            opportunities.append('Price optimization through supplier selection')
        
        # Quality opportunities
        if np.mean(qualities) < 0.8:
            opportunities.append('Quality improvement programs')
        
        # Reliability opportunities
        if np.mean(reliabilities) < 0.8:
            opportunities.append('Supplier development and reliability programs')
        
        # Lead time opportunities
        if np.mean(lead_times) > 30:
            opportunities.append('Supply chain optimization for faster delivery')
        
        return opportunities
    
    def _identify_regional_risks(self, continent_data: List[MarketData]) -> List[str]:
        """Identify regional market risks"""
        risks = []
        
        if not continent_data:
            return ['No supplier data available']
        
        prices = [data.price_usd for data in continent_data]
        qualities = [data.quality_score for data in continent_data]
        reliabilities = [data.reliability_score for data in continent_data]
        lead_times = [data.lead_time_days for data in continent_data]
        
        # Supply concentration risk
        if len(continent_data) < 3:
            risks.append('Limited supplier options - concentration risk')
        
        # Quality risk
        if np.mean(qualities) < 0.7:
            risks.append('Low quality standards - quality risk')
        
        # Reliability risk
        if np.mean(reliabilities) < 0.7:
            risks.append('Low supplier reliability - supply chain risk')
        
        # Price volatility risk
        if np.std(prices) / np.mean(prices) > 0.5:
            risks.append('High price volatility - cost management risk')
        
        # Lead time risk
        if np.mean(lead_times) > 45:
            risks.append('Long lead times - inventory and planning risk')
        
        return risks 