"""
Consumer Marketplace API Routes
Revolutionary consumer marketplace with complete price transparency
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import numpy as np

from app.services.consumer_marketplace_service import SEEKERConsumerMarketplace
from app.database import get_mongo_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/consumer-marketplace", tags=["Consumer Marketplace"])

def get_consumer_marketplace_service():
    """Dependency injection for Consumer Marketplace Service"""
    mongo_client = get_mongo_client()
    return SEEKERConsumerMarketplace(mongo_client)

@router.get("/product-comparison")
async def get_product_comparison(
    product_name: str,
    industry: str,
    category: str,
    marketplace_service: SEEKERConsumerMarketplace = Depends(get_consumer_marketplace_service)
):
    """
    Get comprehensive consumer product comparison with full cost transparency
    """
    try:
        logger.info(f"🛒 Getting consumer comparison for {product_name}")
        
        comparison = await marketplace_service.get_consumer_product_comparison(product_name, industry, category)
        
        return {
            "status": "success",
            "message": f"Consumer comparison generated for {product_name}",
            "data": {
                "product_name": comparison.product_name,
                "industry": comparison.industry,
                "category": comparison.category,
                "top_3_prices": comparison.top_3_prices,
                "price_range": comparison.price_range,
                "average_price": comparison.average_price,
                "best_value_supplier": comparison.best_value_supplier,
                "cost_transparency_rankings": comparison.cost_transparency_rankings,
                "consumer_insights": comparison.consumer_insights,
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating consumer comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison generation failed: {str(e)}")

@router.get("/price-alerts")
async def get_price_alerts(
    product_name: str,
    target_price: float,
    marketplace_service: SEEKERConsumerMarketplace = Depends(get_consumer_marketplace_service)
):
    """
    Get price alerts when products drop below target price
    """
    try:
        logger.info(f"💰 Getting price alerts for {product_name} at ${target_price}")
        
        alerts = await marketplace_service.get_consumer_price_alerts(product_name, target_price)
        
        return {
            "status": "success",
            "message": f"Price alerts generated for {product_name}",
            "data": {
                "product_name": product_name,
                "target_price": target_price,
                "alerts": alerts,
                "alert_count": len(alerts),
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating price alerts: {e}")
        raise HTTPException(status_code=500, detail=f"Price alerts generation failed: {str(e)}")

@router.get("/sustainability-comparison")
async def get_sustainability_comparison(
    product_name: str,
    marketplace_service: SEEKERConsumerMarketplace = Depends(get_consumer_marketplace_service)
):
    """
    Compare products based on sustainability and ethical factors
    """
    try:
        logger.info(f"🌱 Getting sustainability comparison for {product_name}")
        
        comparison = await marketplace_service.get_sustainability_comparison(product_name)
        
        return {
            "status": "success",
            "message": f"Sustainability comparison generated for {product_name}",
            "data": comparison
        }
    except Exception as e:
        logger.error(f"Error generating sustainability comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Sustainability comparison failed: {str(e)}")

@router.get("/cost-transparency")
async def get_cost_transparency_report(
    product_name: str,
    industry: str,
    category: str,
    marketplace_service: SEEKERConsumerMarketplace = Depends(get_consumer_marketplace_service)
):
    """
    Get detailed cost transparency report showing full pricing breakdowns
    """
    try:
        logger.info(f"🔍 Generating cost transparency report for {product_name}")
        
        comparison = await marketplace_service.get_consumer_product_comparison(product_name, industry, category)
        
        # Extract cost transparency data
        transparency_data = []
        for price_data in comparison.top_3_prices:
            transparency_data.append({
                'rank': price_data['rank'],
                'supplier_name': price_data['supplier_name'],
                'continent': price_data['continent'],
                'price_usd': price_data['price_usd'],
                'cost_breakdown': price_data['cost_breakdown'],
                'transparency_score': price_data['cost_breakdown']['cost_transparency_score'],
                'profit_margin_percentage': round(price_data['cost_breakdown']['profit_margin'] / price_data['price_usd'] * 100, 1),
                'retail_markup_percentage': round(price_data['cost_breakdown']['retail_markup'] / price_data['price_usd'] * 100, 1)
            })
        
        return {
            "status": "success",
            "message": f"Cost transparency report generated for {product_name}",
            "data": {
                "product_name": product_name,
                "industry": industry,
                "category": category,
                "transparency_rankings": sorted(transparency_data, key=lambda x: x['transparency_score'], reverse=True),
                "average_transparency": round(np.mean([d['transparency_score'] for d in transparency_data]), 3),
                "transparency_insights": [
                    "Complete cost breakdowns reveal true pricing",
                    "Profit margins and markups clearly displayed",
                    "Consumer empowerment through transparency",
                    "Compare actual costs vs. final prices"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating cost transparency report: {e}")
        raise HTTPException(status_code=500, detail=f"Transparency report failed: {str(e)}")

@router.get("/consumer-insights")
async def get_consumer_insights(
    product_name: str,
    industry: str,
    category: str,
    marketplace_service: SEEKERConsumerMarketplace = Depends(get_consumer_marketplace_service)
):
    """
    Get consumer-focused insights and recommendations
    """
    try:
        logger.info(f"💡 Generating consumer insights for {product_name}")
        
        comparison = await marketplace_service.get_consumer_product_comparison(product_name, industry, category)
        
        return {
            "status": "success",
            "message": f"Consumer insights generated for {product_name}",
            "data": {
                "product_name": product_name,
                "industry": industry,
                "category": category,
                "insights": comparison.consumer_insights,
                "best_value_recommendation": comparison.best_value_supplier,
                "price_analysis": {
                    "price_range": comparison.price_range,
                    "average_price": comparison.average_price,
                    "price_variability": "High" if (comparison.price_range['max'] - comparison.price_range['min']) / comparison.average_price > 0.5 else "Low"
                },
                "transparency_analysis": {
                    "average_transparency": round(np.mean([r['transparency_score'] for r in comparison.cost_transparency_rankings]), 3),
                    "transparency_level": "Excellent" if np.mean([r['transparency_score'] for r in comparison.cost_transparency_rankings]) > 0.8 else "Good" if np.mean([r['transparency_score'] for r in comparison.cost_transparency_rankings]) > 0.6 else "Poor"
                },
                "consumer_recommendations": [
                    "Compare total costs, not just final prices",
                    "Consider quality-to-price ratios",
                    "Look for transparent pricing breakdowns",
                    "Check sustainability scores",
                    "Read consumer reviews and ratings"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating consumer insights: {e}")
        raise HTTPException(status_code=500, detail=f"Consumer insights failed: {str(e)}")

@router.get("/global-pricing-trends")
async def get_global_pricing_trends(
    industry: str,
    category: str,
    marketplace_service: SEEKERConsumerMarketplace = Depends(get_consumer_marketplace_service)
):
    """
    Get global pricing trends and market analysis
    """
    try:
        logger.info(f"📊 Generating global pricing trends for {industry} - {category}")
        
        # Sample product for trend analysis
        sample_product = f"Sample {category}"
        comparison = await marketplace_service.get_consumer_product_comparison(sample_product, industry, category)
        
        # Analyze pricing by continent
        continent_pricing = {}
        for price_data in comparison.top_3_prices:
            continent = price_data['continent']
            if continent not in continent_pricing:
                continent_pricing[continent] = []
            continent_pricing[continent].append(price_data['price_usd'])
        
        continent_analysis = {}
        for continent, prices in continent_pricing.items():
            continent_analysis[continent] = {
                'average_price': round(np.mean(prices), 2),
                'price_range': {'min': min(prices), 'max': max(prices)},
                'price_volatility': round(np.std(prices), 2),
                'supplier_count': len(prices)
            }
        
        return {
            "status": "success",
            "message": f"Global pricing trends generated for {industry} - {category}",
            "data": {
                "industry": industry,
                "category": category,
                "continent_analysis": continent_analysis,
                "global_insights": [
                    "Pricing varies significantly by region",
                    "Transportation costs impact final prices",
                    "Local regulations affect pricing structures",
                    "Currency fluctuations influence costs",
                    "Supply chain efficiency varies by continent"
                ],
                "trend_recommendations": [
                    "Consider total landed costs, not just product prices",
                    "Factor in shipping and import duties",
                    "Compare quality standards across regions",
                    "Evaluate supplier reliability and delivery times",
                    "Check for regional certifications and compliance"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating global pricing trends: {e}")
        raise HTTPException(status_code=500, detail=f"Pricing trends failed: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check for Consumer Marketplace service
    """
    return {
        "status": "success",
        "message": "Consumer Marketplace service is healthy",
        "service": "SEEKER Consumer Marketplace",
        "version": "1.0.0",
        "features": [
            "Complete price transparency",
            "Cost breakdown analysis",
            "Consumer-focused insights",
            "Global pricing comparison",
            "Sustainability rankings",
            "Price alerts and monitoring"
        ]
    } 