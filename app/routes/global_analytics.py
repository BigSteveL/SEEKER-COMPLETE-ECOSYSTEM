"""
Global Analytics API Routes
Handles global market intelligence and supplier analysis requests
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from app.services.global_analytics_service import SEEKERGlobalAnalyticsService, Continent
from app.database import get_mongo_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/global-analytics", tags=["Global Analytics"])

def get_global_analytics_service():
    """Dependency injection for Global Analytics Service"""
    mongo_client = get_mongo_client()
    return SEEKERGlobalAnalyticsService(mongo_client)

@router.post("/analyze-market")
async def analyze_global_market(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Perform comprehensive global market analysis for specified industry and product category
    """
    try:
        logger.info(f"🔍 Starting global market analysis for {industry} - {product_category}")
        
        result = await analytics_service.analyze_global_market(industry, product_category)
        
        return {
            "status": "success",
            "message": f"Global market analysis completed for {industry} - {product_category}",
            "data": {
                "industry": industry,
                "product_category": product_category,
                "analysis_timestamp": datetime.now().isoformat(),
                "market_penetration": result.market_penetration,
                "opportunity_score": result.opportunity_score,
                "competitive_landscape": result.competitive_landscape,
                "price_quality_matrix": result.price_quality_matrix,
                "supply_chain_routes": result.supply_chain_routes,
                "compliance_status": result.compliance_status
            }
        }
    except Exception as e:
        logger.error(f"Error in global market analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/heatmap-data")
async def get_global_heatmap_data(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Get global heatmap data for visualization
    """
    try:
        logger.info(f"🗺️ Generating heatmap data for {industry} - {product_category}")
        
        heatmap_data = await analytics_service.get_global_heatmap_data(industry, product_category)
        
        return {
            "status": "success",
            "message": f"Heatmap data generated for {industry} - {product_category}",
            "data": heatmap_data
        }
    except Exception as e:
        logger.error(f"Error generating heatmap data: {e}")
        raise HTTPException(status_code=500, detail=f"Heatmap generation failed: {str(e)}")

@router.get("/supplier-reliability")
async def get_supplier_reliability_scores(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Get supplier reliability scores for visualization
    """
    try:
        logger.info(f"📊 Getting supplier reliability scores for {industry} - {product_category}")
        
        suppliers = await analytics_service.get_supplier_reliability_scores(industry, product_category)
        
        return {
            "status": "success",
            "message": f"Supplier reliability data retrieved for {industry} - {product_category}",
            "data": {
                "suppliers": suppliers,
                "total_suppliers": len(suppliers),
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting supplier reliability scores: {e}")
        raise HTTPException(status_code=500, detail=f"Supplier data retrieval failed: {str(e)}")

@router.get("/continents")
async def get_available_continents():
    """
    Get list of available continents for analysis
    """
    continents = [
        {
            "id": continent.value,
            "name": continent.value.replace("_", " ").title(),
            "description": f"Market data for {continent.value.replace('_', ' ').title()}"
        }
        for continent in Continent
    ]
    
    return {
        "status": "success",
        "message": "Available continents retrieved",
        "data": {
            "continents": continents,
            "total_continents": len(continents)
        }
    }

@router.get("/data-sources")
async def get_data_sources():
    """
    Get available data sources for global analytics
    """
    data_sources = [
        {
            "id": "manufacturer_database",
            "name": "Manufacturer Database",
            "description": "Direct manufacturer and supplier databases"
        },
        {
            "id": "industry_association",
            "name": "Industry Association",
            "description": "Industry association member directories"
        },
        {
            "id": "government_trade",
            "name": "Government Trade Data",
            "description": "Official government trade and import/export data"
        },
        {
            "id": "business_directory",
            "name": "Business Directory",
            "description": "Local and regional business directories"
        },
        {
            "id": "pricing_feed",
            "name": "Real-time Pricing Feed",
            "description": "Live pricing data from global markets"
        }
    ]
    
    return {
        "status": "success",
        "message": "Available data sources retrieved",
        "data": {
            "data_sources": data_sources,
            "total_sources": len(data_sources)
        }
    }

@router.post("/collect-market-data")
async def collect_market_data(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Collect fresh market data from all global sources
    """
    try:
        logger.info(f"📊 Collecting market data for {industry} - {product_category}")
        
        market_data = await analytics_service.collect_global_market_data(industry, product_category)
        
        return {
            "status": "success",
            "message": f"Market data collection completed for {industry} - {product_category}",
            "data": {
                "total_records": len(market_data),
                "continents_covered": len(set(data.continent.value for data in market_data)),
                "data_sources": list(set(data.data_source.value for data in market_data)),
                "collection_timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error collecting market data: {e}")
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

@router.get("/market-summary")
async def get_market_summary(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Get comprehensive market summary with key metrics
    """
    try:
        logger.info(f"📋 Generating market summary for {industry} - {product_category}")
        
        # Get latest analytics result
        result = await analytics_service.analyze_global_market(industry, product_category)
        
        # Calculate additional summary metrics
        competitive_landscape = result.competitive_landscape
        total_suppliers = sum(data['supplier_count'] for data in competitive_landscape.values())
        avg_price = sum(data['avg_price'] * data['supplier_count'] for data in competitive_landscape.values()) / total_suppliers if total_suppliers > 0 else 0
        
        summary = {
            "industry": industry,
            "product_category": product_category,
            "market_penetration": result.market_penetration,
            "opportunity_score": result.opportunity_score,
            "total_suppliers": total_suppliers,
            "continents_covered": len(competitive_landscape),
            "average_price_usd": round(avg_price, 2),
            "compliance_rate": sum(result.compliance_status.values()) / len(result.compliance_status) * 100,
            "top_suppliers": list(result.price_quality_matrix.keys())[:5],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "message": f"Market summary generated for {industry} - {product_category}",
            "data": summary
        }
    except Exception as e:
        logger.error(f"Error generating market summary: {e}")
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check for Global Analytics service
    """
    return {
        "status": "healthy",
        "service": "Global Analytics Validation System",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    } 

@router.get("/advanced-insights")
async def get_advanced_market_insights(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Get advanced market insights with comprehensive competitive analysis
    """
    try:
        logger.info(f"🔍 Generating advanced market insights for {industry} - {product_category}")
        
        insights = await analytics_service.get_advanced_market_insights(industry, product_category)
        
        return {
            "status": "success",
            "message": f"Advanced market insights generated for {industry} - {product_category}",
            "data": insights
        }
    except Exception as e:
        logger.error(f"Error generating advanced insights: {e}")
        raise HTTPException(status_code=500, detail=f"Advanced insights generation failed: {str(e)}")

@router.get("/market-intelligence")
async def get_market_intelligence_report(
    industry: str,
    product_category: str,
    analytics_service: SEEKERGlobalAnalyticsService = Depends(get_global_analytics_service)
):
    """
    Get comprehensive market intelligence report
    """
    try:
        logger.info(f"📊 Generating market intelligence report for {industry} - {product_category}")
        
        # Get basic analysis
        basic_analysis = await analytics_service.analyze_global_market(industry, product_category)
        
        # Get advanced insights
        advanced_insights = await analytics_service.get_advanced_market_insights(industry, product_category)
        
        # Compile comprehensive report
        report = {
            "executive_summary": {
                "industry": industry,
                "product_category": product_category,
                "analysis_timestamp": datetime.now().isoformat(),
                "market_penetration": basic_analysis.market_penetration,
                "opportunity_score": basic_analysis.opportunity_score,
                "overall_risk_level": advanced_insights['risk_assessment']['risk_level']
            },
            "market_overview": advanced_insights['market_overview'],
            "competitive_analysis": advanced_insights['competitive_analysis'],
            "supply_chain_optimization": advanced_insights['supply_chain_optimization'],
            "risk_assessment": advanced_insights['risk_assessment'],
            "opportunity_mapping": advanced_insights['opportunity_mapping'],
            "trend_analysis": advanced_insights['trend_analysis'],
            "regional_insights": advanced_insights['regional_insights'],
            "strategic_recommendations": {
                "immediate_actions": [
                    "Review top 5 suppliers by cost-quality ratio",
                    "Assess high-risk suppliers and develop mitigation plans",
                    "Evaluate geographic expansion opportunities"
                ],
                "medium_term_strategies": [
                    "Implement supplier development programs",
                    "Establish quality assurance partnerships",
                    "Develop long-term supply agreements"
                ],
                "long_term_goals": [
                    "Achieve 7-continent supplier coverage",
                    "Maintain 90%+ supplier reliability",
                    "Optimize total cost of ownership"
                ]
            }
        }
        
        return {
            "status": "success",
            "message": f"Market intelligence report generated for {industry} - {product_category}",
            "data": report
        }
    except Exception as e:
        logger.error(f"Error generating market intelligence report: {e}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}") 