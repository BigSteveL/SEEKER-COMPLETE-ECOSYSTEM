"""
SEEKER Consumer Marketplace Service
Revolutionary global consumer marketplace with complete price transparency
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

class CostComponent(Enum):
    MATERIAL_COST = "material_cost"
    LABOR_COST = "labor_cost"
    TRANSPORTATION_COST = "transportation_cost"
    TARIFF_COST = "tariff_cost"
    OVERHEAD_COST = "overhead_cost"
    PROFIT_MARGIN = "profit_margin"
    RETAIL_MARKUP = "retail_markup"

@dataclass
class CostBreakdown:
    material_cost: float
    labor_cost: float
    transportation_cost: float
    tariff_cost: float
    overhead_cost: float
    profit_margin: float
    retail_markup: float
    total_cost: float
    final_price: float
    cost_transparency_score: float

@dataclass
class ConsumerProduct:
    product_id: str
    product_name: str
    industry: str
    category: str
    continent: Continent
    country: str
    supplier_name: str
    supplier_rating: float
    price_usd: float
    cost_breakdown: CostBreakdown
    quality_score: float
    delivery_time_days: int
    warranty_months: int
    consumer_rating: float
    review_count: int
    sustainability_score: float
    last_updated: datetime

@dataclass
class MarketComparison:
    product_name: str
    industry: str
    category: str
    top_3_prices: List[Dict[str, Any]]
    price_range: Dict[str, float]
    average_price: float
    best_value_supplier: Dict[str, Any]
    cost_transparency_rankings: List[Dict[str, Any]]
    consumer_insights: List[str]

class SEEKERConsumerMarketplace:
    """
    Revolutionary Consumer Marketplace with Complete Price Transparency
    """
    
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.db = mongo_client.seeker_consumer_marketplace
        self.collections = {
            'products': self.db.products,
            'cost_breakdowns': self.db.cost_breakdowns,
            'market_comparisons': self.db.market_comparisons,
            'consumer_reviews': self.db.consumer_reviews,
            'supplier_ratings': self.db.supplier_ratings
        }
        
        # Consumer-focused data sources
        self.consumer_data_sources = {
            Continent.NORTH_AMERICA: {
                'consumer_reports': 'https://api.consumerreports.org/v1',
                'amazon_pricing': 'https://api.amazon-pricing.com/v1',
                'walmart_pricing': 'https://api.walmart-pricing.com/v1',
                'costco_pricing': 'https://api.costco-pricing.com/v1',
                'target_pricing': 'https://api.target-pricing.com/v1'
            },
            Continent.EUROPE: {
                'eu_consumer_data': 'https://api.eu-consumer.org/v1',
                'amazon_eu': 'https://api.amazon-eu.com/v1',
                'ikea_pricing': 'https://api.ikea-pricing.com/v1',
                'carrefour_pricing': 'https://api.carrefour-pricing.com/v1',
                'tesco_pricing': 'https://api.tesco-pricing.com/v1'
            },
            Continent.ASIA: {
                'asia_consumer_data': 'https://api.asia-consumer.org/v1',
                'alibaba_pricing': 'https://api.alibaba-pricing.com/v1',
                'jd_pricing': 'https://api.jd-pricing.com/v1',
                'rakuten_pricing': 'https://api.rakuten-pricing.com/v1',
                'lazada_pricing': 'https://api.lazada-pricing.com/v1'
            },
            Continent.SOUTH_AMERICA: {
                'sa_consumer_data': 'https://api.sa-consumer.org/v1',
                'mercado_libre': 'https://api.mercadolibre.com/v1',
                'b2w_pricing': 'https://api.b2w-pricing.com/v1',
                'magazine_luiza': 'https://api.magazineluiza.com/v1'
            },
            Continent.AFRICA: {
                'africa_consumer_data': 'https://api.africa-consumer.org/v1',
                'jumia_pricing': 'https://api.jumia-pricing.com/v1',
                'takealot_pricing': 'https://api.takealot-pricing.com/v1',
                'konga_pricing': 'https://api.konga-pricing.com/v1'
            },
            Continent.AUSTRALIA_OCEANIA: {
                'au_consumer_data': 'https://api.au-consumer.org/v1',
                'amazon_au': 'https://api.amazon-au.com/v1',
                'ebay_au': 'https://api.ebay-au.com/v1',
                'catch_pricing': 'https://api.catch-pricing.com/v1'
            },
            Continent.ANTARCTICA: {
                'research_supplies': 'https://api.antarctica-supplies.com/v1',
                'specialized_equipment': 'https://api.antarctica-equipment.com/v1'
            }
        }
        
        logger.info("🛒 SEEKER Consumer Marketplace initialized")
    
    async def get_consumer_product_comparison(self, product_name: str, industry: str, category: str) -> MarketComparison:
        """
        Get comprehensive consumer product comparison with full cost transparency
        """
        logger.info(f"🛒 Getting consumer comparison for {product_name} in {industry} - {category}")
        
        # Collect product data from all continents
        all_products = await self.collect_consumer_products(product_name, industry, category)
        
        if not all_products:
            raise HTTPException(status_code=404, detail="No products found for comparison")
        
        # Generate cost breakdowns for all products
        products_with_costs = []
        for product in all_products:
            cost_breakdown = await self.generate_cost_breakdown(product)
            product.cost_breakdown = cost_breakdown
            products_with_costs.append(product)
        
        # Find top 3 best prices
        sorted_products = sorted(products_with_costs, key=lambda p: p.price_usd)
        top_3_prices = []
        
        for i, product in enumerate(sorted_products[:3]):
            top_3_prices.append({
                'rank': i + 1,
                'supplier_name': product.supplier_name,
                'continent': product.continent.value,
                'country': product.country,
                'price_usd': product.price_usd,
                'cost_breakdown': {
                    'material_cost': product.cost_breakdown.material_cost,
                    'labor_cost': product.cost_breakdown.labor_cost,
                    'transportation_cost': product.cost_breakdown.transportation_cost,
                    'tariff_cost': product.cost_breakdown.tariff_cost,
                    'overhead_cost': product.cost_breakdown.overhead_cost,
                    'profit_margin': product.cost_breakdown.profit_margin,
                    'retail_markup': product.cost_breakdown.retail_markup,
                    'total_cost': product.cost_breakdown.total_cost,
                    'final_price': product.cost_breakdown.final_price,
                    'cost_transparency_score': product.cost_breakdown.cost_transparency_score
                },
                'quality_score': product.quality_score,
                'delivery_time': product.delivery_time_days,
                'consumer_rating': product.consumer_rating,
                'sustainability_score': product.sustainability_score
            })
        
        # Calculate price statistics
        prices = [p.price_usd for p in products_with_costs]
        price_range = {
            'min': min(prices),
            'max': max(prices),
            'median': np.median(prices)
        }
        average_price = np.mean(prices)
        
        # Find best value supplier (price/quality ratio)
        best_value_supplier = None
        best_value_score = 0
        
        for product in products_with_costs:
            value_score = product.quality_score / (product.price_usd / 1000)
            if value_score > best_value_score:
                best_value_score = value_score
                best_value_supplier = {
                    'supplier_name': product.supplier_name,
                    'continent': product.continent.value,
                    'country': product.country,
                    'price_usd': product.price_usd,
                    'quality_score': product.quality_score,
                    'value_score': round(value_score, 3),
                    'cost_breakdown': {
                        'material_cost': product.cost_breakdown.material_cost,
                        'labor_cost': product.cost_breakdown.labor_cost,
                        'transportation_cost': product.cost_breakdown.transportation_cost,
                        'tariff_cost': product.cost_breakdown.tariff_cost,
                        'overhead_cost': product.cost_breakdown.overhead_cost,
                        'profit_margin': product.cost_breakdown.profit_margin,
                        'retail_markup': product.cost_breakdown.retail_markup,
                        'total_cost': product.cost_breakdown.total_cost,
                        'final_price': product.cost_breakdown.final_price
                    }
                }
        
        # Generate cost transparency rankings
        cost_transparency_rankings = []
        for product in sorted(products_with_costs, key=lambda p: p.cost_breakdown.cost_transparency_score, reverse=True):
            cost_transparency_rankings.append({
                'rank': len(cost_transparency_rankings) + 1,
                'supplier_name': product.supplier_name,
                'continent': product.continent.value,
                'transparency_score': product.cost_breakdown.cost_transparency_score,
                'price_usd': product.price_usd,
                'profit_margin': product.cost_breakdown.profit_margin,
                'retail_markup': product.cost_breakdown.retail_markup
            })
        
        # Generate consumer insights
        consumer_insights = self.generate_consumer_insights(products_with_costs)
        
        comparison = MarketComparison(
            product_name=product_name,
            industry=industry,
            category=category,
            top_3_prices=top_3_prices,
            price_range=price_range,
            average_price=round(average_price, 2),
            best_value_supplier=best_value_supplier,
            cost_transparency_rankings=cost_transparency_rankings,
            consumer_insights=consumer_insights
        )
        
        # Store comparison in database
        await self.store_market_comparison(comparison)
        
        return comparison
    
    async def collect_consumer_products(self, product_name: str, industry: str, category: str) -> List[ConsumerProduct]:
        """
        Collect consumer product data from all continents
        """
        logger.info(f"🛒 Collecting consumer products for {product_name}")
        
        all_products = []
        
        # Collect from all continents concurrently
        tasks = []
        for continent in Continent:
            task = self.collect_continental_products(continent, product_name, industry, category)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_products.extend(result)
            else:
                logger.error(f"Error collecting products: {result}")
        
        logger.info(f"✅ Collected {len(all_products)} consumer products globally")
        return all_products
    
    async def collect_continental_products(self, continent: Continent, product_name: str, industry: str, category: str) -> List[ConsumerProduct]:
        """
        Collect consumer products from specific continent
        """
        logger.info(f"🌍 Collecting consumer products from {continent.value}")
        
        products = []
        
        try:
            # Simulate API calls to consumer data sources
            async with aiohttp.ClientSession() as session:
                # Consumer reports data
                consumer_data = await self.fetch_consumer_reports_data(session, continent, product_name, industry, category)
                products.extend(consumer_data)
                
                # E-commerce pricing data
                ecommerce_data = await self.fetch_ecommerce_pricing_data(session, continent, product_name, industry, category)
                products.extend(ecommerce_data)
                
                # Retail pricing data
                retail_data = await self.fetch_retail_pricing_data(session, continent, product_name, industry, category)
                products.extend(retail_data)
                
        except Exception as e:
            logger.error(f"Error collecting products from {continent.value}: {e}")
        
        return products
    
    async def fetch_consumer_reports_data(self, session: aiohttp.ClientSession, continent: Continent, product_name: str, industry: str, category: str) -> List[ConsumerProduct]:
        """Fetch consumer reports and ratings data"""
        await asyncio.sleep(0.1)  # Simulate network delay
        
        products = []
        for i in range(3):  # Generate 3 sample products per continent
            product = ConsumerProduct(
                product_id=f"CR_{continent.value}_{i}",
                product_name=product_name,
                industry=industry,
                category=category,
                continent=continent,
                country=self.get_sample_country(continent),
                supplier_name=f"{continent.value.title()} Consumer Supplier {i}",
                supplier_rating=round(np.random.uniform(3.5, 5.0), 1),
                price_usd=round(np.random.uniform(50, 2000), 2),
                cost_breakdown=None,  # Will be generated later
                quality_score=round(np.random.uniform(0.7, 0.95), 2),
                delivery_time_days=np.random.randint(3, 30),
                warranty_months=np.random.randint(6, 36),
                consumer_rating=round(np.random.uniform(3.0, 5.0), 1),
                review_count=np.random.randint(10, 1000),
                sustainability_score=round(np.random.uniform(0.5, 0.9), 2),
                last_updated=datetime.now()
            )
            products.append(product)
        
        return products
    
    async def fetch_ecommerce_pricing_data(self, session: aiohttp.ClientSession, continent: Continent, product_name: str, industry: str, category: str) -> List[ConsumerProduct]:
        """Fetch e-commerce pricing data"""
        await asyncio.sleep(0.1)
        
        products = []
        for i in range(2):  # Generate 2 sample products per continent
            product = ConsumerProduct(
                product_id=f"EC_{continent.value}_{i}",
                product_name=product_name,
                industry=industry,
                category=category,
                continent=continent,
                country=self.get_sample_country(continent),
                supplier_name=f"{continent.value.title()} E-commerce Supplier {i}",
                supplier_rating=round(np.random.uniform(3.0, 4.8), 1),
                price_usd=round(np.random.uniform(40, 1800), 2),
                cost_breakdown=None,
                quality_score=round(np.random.uniform(0.6, 0.9), 2),
                delivery_time_days=np.random.randint(5, 25),
                warranty_months=np.random.randint(3, 24),
                consumer_rating=round(np.random.uniform(2.5, 4.9), 1),
                review_count=np.random.randint(5, 500),
                sustainability_score=round(np.random.uniform(0.4, 0.8), 2),
                last_updated=datetime.now()
            )
            products.append(product)
        
        return products
    
    async def fetch_retail_pricing_data(self, session: aiohttp.ClientSession, continent: Continent, product_name: str, industry: str, category: str) -> List[ConsumerProduct]:
        """Fetch retail pricing data"""
        await asyncio.sleep(0.1)
        
        products = []
        for i in range(2):  # Generate 2 sample products per continent
            product = ConsumerProduct(
                product_id=f"RT_{continent.value}_{i}",
                product_name=product_name,
                industry=industry,
                category=category,
                continent=continent,
                country=self.get_sample_country(continent),
                supplier_name=f"{continent.value.title()} Retail Supplier {i}",
                supplier_rating=round(np.random.uniform(3.2, 4.6), 1),
                price_usd=round(np.random.uniform(60, 2200), 2),
                cost_breakdown=None,
                quality_score=round(np.random.uniform(0.65, 0.88), 2),
                delivery_time_days=np.random.randint(2, 15),
                warranty_months=np.random.randint(6, 48),
                consumer_rating=round(np.random.uniform(3.2, 4.7), 1),
                review_count=np.random.randint(20, 800),
                sustainability_score=round(np.random.uniform(0.3, 0.7), 2),
                last_updated=datetime.now()
            )
            products.append(product)
        
        return products
    
    async def generate_cost_breakdown(self, product: ConsumerProduct) -> CostBreakdown:
        """
        Generate detailed cost breakdown for consumer transparency
        """
        # Base material cost (40-60% of total cost)
        material_cost = product.price_usd * np.random.uniform(0.4, 0.6)
        
        # Labor cost (15-25% of total cost)
        labor_cost = product.price_usd * np.random.uniform(0.15, 0.25)
        
        # Transportation cost (5-15% of total cost)
        transportation_cost = product.price_usd * np.random.uniform(0.05, 0.15)
        
        # Tariff cost (0-10% of total cost)
        tariff_cost = product.price_usd * np.random.uniform(0.0, 0.10)
        
        # Overhead cost (10-20% of total cost)
        overhead_cost = product.price_usd * np.random.uniform(0.10, 0.20)
        
        # Profit margin (5-20% of total cost)
        profit_margin = product.price_usd * np.random.uniform(0.05, 0.20)
        
        # Retail markup (10-30% of total cost)
        retail_markup = product.price_usd * np.random.uniform(0.10, 0.30)
        
        # Calculate total cost
        total_cost = material_cost + labor_cost + transportation_cost + tariff_cost + overhead_cost
        
        # Calculate final price
        final_price = total_cost + profit_margin + retail_markup
        
        # Calculate cost transparency score (0-1)
        # Higher score = more transparent pricing
        transparency_factors = [
            product.quality_score,  # Higher quality often means better transparency
            min(profit_margin / product.price_usd, 0.15) / 0.15,  # Lower profit margin = better transparency
            min(retail_markup / product.price_usd, 0.20) / 0.20,  # Lower markup = better transparency
            product.consumer_rating / 5.0,  # Higher consumer rating = better transparency
            product.sustainability_score  # Higher sustainability = better transparency
        ]
        cost_transparency_score = np.mean(transparency_factors)
        
        return CostBreakdown(
            material_cost=round(material_cost, 2),
            labor_cost=round(labor_cost, 2),
            transportation_cost=round(transportation_cost, 2),
            tariff_cost=round(tariff_cost, 2),
            overhead_cost=round(overhead_cost, 2),
            profit_margin=round(profit_margin, 2),
            retail_markup=round(retail_markup, 2),
            total_cost=round(total_cost, 2),
            final_price=round(final_price, 2),
            cost_transparency_score=round(cost_transparency_score, 3)
        )
    
    def generate_consumer_insights(self, products: List[ConsumerProduct]) -> List[str]:
        """
        Generate consumer-focused insights about pricing and transparency
        """
        insights = []
        
        if not products:
            return ["No products available for analysis"]
        
        # Price analysis insights
        prices = [p.price_usd for p in products]
        price_cv = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0
        
        if price_cv > 0.4:
            insights.append(f"⚠️ High price variability ({round(price_cv * 100, 1)}% difference) - shop around for best deals")
        else:
            insights.append("✅ Stable pricing across suppliers - consistent market pricing")
        
        # Cost transparency insights
        transparency_scores = [p.cost_breakdown.cost_transparency_score for p in products]
        avg_transparency = np.mean(transparency_scores)
        
        if avg_transparency > 0.8:
            insights.append("✅ Excellent cost transparency - suppliers clearly show pricing breakdowns")
        elif avg_transparency > 0.6:
            insights.append("⚠️ Moderate cost transparency - some suppliers hide pricing details")
        else:
            insights.append("❌ Poor cost transparency - suppliers not showing full pricing breakdowns")
        
        # Profit margin insights
        profit_margins = [p.cost_breakdown.profit_margin for p in products]
        avg_profit_margin = np.mean(profit_margins)
        
        if avg_profit_margin > product.price_usd * 0.15:
            insights.append(f"💰 High profit margins detected - suppliers making {round(avg_profit_margin / product.price_usd * 100, 1)}% profit")
        else:
            insights.append("✅ Reasonable profit margins - fair pricing for consumers")
        
        # Quality vs price insights
        quality_price_ratios = [(p.quality_score / (p.price_usd / 1000)) for p in products]
        best_ratio = max(quality_price_ratios)
        worst_ratio = min(quality_price_ratios)
        
        if best_ratio > worst_ratio * 2:
            insights.append("🎯 Significant quality-price differences - some suppliers offer much better value")
        
        # Geographic insights
        continent_prices = {}
        for product in products:
            if product.continent.value not in continent_prices:
                continent_prices[product.continent.value] = []
            continent_prices[product.continent.value].append(product.price_usd)
        
        cheapest_continent = min(continent_prices.items(), key=lambda x: np.mean(x[1]))
        most_expensive_continent = max(continent_prices.items(), key=lambda x: np.mean(x[1]))
        
        if cheapest_continent[0] != most_expensive_continent[0]:
            insights.append(f"🌍 {cheapest_continent[0].replace('_', ' ').title()} offers best prices, {most_expensive_continent[0].replace('_', ' ').title()} most expensive")
        
        return insights
    
    def get_sample_country(self, continent: Continent) -> str:
        """Get sample country for continent"""
        countries = {
            Continent.NORTH_AMERICA: ['USA', 'Canada', 'Mexico'],
            Continent.EUROPE: ['Germany', 'France', 'UK', 'Italy', 'Spain'],
            Continent.ASIA: ['China', 'Japan', 'South Korea', 'India', 'Singapore'],
            Continent.SOUTH_AMERICA: ['Brazil', 'Argentina', 'Chile', 'Colombia'],
            Continent.AFRICA: ['South Africa', 'Nigeria', 'Kenya', 'Egypt'],
            Continent.AUSTRALIA_OCEANIA: ['Australia', 'New Zealand'],
            Continent.ANTARCTICA: ['Research Station']
        }
        return np.random.choice(countries[continent])
    
    async def store_market_comparison(self, comparison: MarketComparison):
        """Store market comparison in database"""
        doc = {
            'product_name': comparison.product_name,
            'industry': comparison.industry,
            'category': comparison.category,
            'top_3_prices': comparison.top_3_prices,
            'price_range': comparison.price_range,
            'average_price': comparison.average_price,
            'best_value_supplier': comparison.best_value_supplier,
            'cost_transparency_rankings': comparison.cost_transparency_rankings,
            'consumer_insights': comparison.consumer_insights,
            'analysis_timestamp': datetime.now()
        }
        
        await self.collections['market_comparisons'].insert_one(doc)
    
    async def get_consumer_price_alerts(self, product_name: str, target_price: float) -> List[Dict[str, Any]]:
        """
        Get price alerts when products drop below target price
        """
        # Get current market comparison
        comparison = await self.get_consumer_product_comparison(product_name, "General", "Consumer Goods")
        
        alerts = []
        for price_data in comparison.top_3_prices:
            if price_data['price_usd'] <= target_price:
                alerts.append({
                    'alert_type': 'price_drop',
                    'product_name': product_name,
                    'supplier_name': price_data['supplier_name'],
                    'current_price': price_data['price_usd'],
                    'target_price': target_price,
                    'savings': target_price - price_data['price_usd'],
                    'continent': price_data['continent'],
                    'quality_score': price_data['quality_score'],
                    'consumer_rating': price_data['consumer_rating']
                })
        
        return alerts
    
    async def get_sustainability_comparison(self, product_name: str) -> Dict[str, Any]:
        """
        Compare products based on sustainability and ethical factors
        """
        products = await self.collect_consumer_products(product_name, "General", "Consumer Goods")
        
        if not products:
            return {"error": "No products found"}
        
        # Sort by sustainability score
        sustainable_products = sorted(products, key=lambda p: p.sustainability_score, reverse=True)
        
        return {
            'product_name': product_name,
            'sustainability_rankings': [
                {
                    'rank': i + 1,
                    'supplier_name': p.supplier_name,
                    'continent': p.continent.value,
                    'sustainability_score': p.sustainability_score,
                    'price_usd': p.price_usd,
                    'quality_score': p.quality_score,
                    'consumer_rating': p.consumer_rating
                }
                for i, p in enumerate(sustainable_products[:5])
            ],
            'average_sustainability': round(np.mean([p.sustainability_score for p in products]), 3),
            'sustainability_insights': self.generate_sustainability_insights(products)
        }
    
    def generate_sustainability_insights(self, products: List[ConsumerProduct]) -> List[str]:
        """Generate sustainability-focused insights"""
        insights = []
        
        sustainability_scores = [p.sustainability_score for p in products]
        avg_sustainability = np.mean(sustainability_scores)
        
        if avg_sustainability > 0.8:
            insights.append("🌱 Excellent sustainability practices across suppliers")
        elif avg_sustainability > 0.6:
            insights.append("🌿 Good sustainability practices - most suppliers eco-friendly")
        else:
            insights.append("⚠️ Limited sustainability practices - consider eco-friendly alternatives")
        
        # Find most sustainable supplier
        most_sustainable = max(products, key=lambda p: p.sustainability_score)
        insights.append(f"🏆 {most_sustainable.supplier_name} leads in sustainability (score: {most_sustainable.sustainability_score})")
        
        return insights 