"""
Global Shipping Marketplace API Routes
Revolutionary shipping transparency with daily volume bidding system
Consumer-first global logistics optimization across all 7 continents
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import numpy as np

from app.services.global_shipping_service import SEEKERGlobalShippingService, ShippingService
from app.database import get_mongo_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/global-shipping", tags=["Global Shipping Marketplace"])

def get_global_shipping_service():
    """Dependency injection for Global Shipping Service"""
    try:
        mongo_client = get_mongo_client()
        return SEEKERGlobalShippingService(mongo_client)
    except Exception as e:
        logger.warning(f"MongoDB client not available, using demo mode: {e}")
        return SEEKERGlobalShippingService(None)

@router.get("/shipping-quote")
async def get_consumer_shipping_quote(
    origin: str,
    destination: str,
    weight_kg: float,
    volume_cm3: float,
    service_type: str,
    shipping_service: SEEKERGlobalShippingService = Depends(get_global_shipping_service)
):
    """
    Get revolutionary consumer shipping quote with volume bidding advantages
    """
    try:
        logger.info(f"🚢 Getting shipping quote: {origin} → {destination}")
        
        # Convert service type string to enum
        try:
            service_enum = ShippingService(service_type.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid service type: {service_type}")
        
        quote = await shipping_service.get_consumer_shipping_quote(
            origin, destination, weight_kg, volume_cm3, service_enum
        )
        
        return {
            "status": "success",
            "message": f"Shipping quote generated for {origin} → {destination}",
            "data": {
                "origin": quote.origin,
                "destination": quote.destination,
                "weight_kg": quote.weight_kg,
                "volume_cm3": quote.volume_cm3,
                "service_type": quote.service_type.value,
                "top_3_carriers": quote.top_3_carriers,
                "volume_advantage_savings": quote.volume_advantage_savings,
                "transparency_breakdown": quote.transparency_breakdown,
                "delivery_options": quote.delivery_options,
                "sustainability_ranking": quote.sustainability_ranking,
                "quote_timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating shipping quote: {e}")
        raise HTTPException(status_code=500, detail=f"Shipping quote generation failed: {str(e)}")

@router.get("/daily-volume-bidding")
async def get_daily_volume_bidding(
    origin_continent: str,
    destination_continent: str,
    shipping_service: SEEKERGlobalShippingService = Depends(get_global_shipping_service)
):
    """
    Get daily volume aggregation and competitive bidding results
    """
    try:
        logger.info(f"📦 Getting daily volume bidding: {origin_continent} → {destination_continent}")
        
        aggregation = await shipping_service.aggregate_daily_shipping_volume(
            origin_continent, destination_continent
        )
        
        # Format carrier bids for response
        formatted_bids = []
        for bid in aggregation.best_bids:
            formatted_bid = {
                'carrier': bid.carrier.value.upper(),
                'service_type': bid.service_type.value,
                'base_rate_usd': round(bid.base_rate_usd, 2),
                'volume_discount_percentage': round(bid.volume_discount_percentage, 1),
                'final_rate_usd': round(bid.final_rate_usd, 2),
                'delivery_days': bid.delivery_days,
                'reliability_score': round(bid.reliability_score, 3),
                'sustainability_score': round(bid.sustainability_score, 3),
                'daily_volume_requirement': bid.daily_volume_requirement,
                'bid_status': bid.status.value,
                'bid_expiry': bid.bid_expiry.isoformat()
            }
            formatted_bids.append(formatted_bid)
        
        return {
            "status": "success",
            "message": f"Daily volume bidding results for {origin_continent} → {destination_continent}",
            "data": {
                "date": aggregation.date.isoformat(),
                "origin_continent": aggregation.origin_continent,
                "destination_continent": aggregation.destination_continent,
                "total_weight_kg": round(aggregation.total_weight_kg, 2),
                "total_volume_cm3": round(aggregation.total_volume_cm3, 2),
                "total_packages": aggregation.total_packages,
                "average_package_weight": round(aggregation.average_package_weight, 2),
                "shipping_requirements": aggregation.shipping_requirements,
                "carrier_bids_count": len(aggregation.carrier_bids),
                "best_bids": formatted_bids,
                "bidding_insights": [
                    "Carriers compete for daily volume to offer best rates",
                    "Volume discounts range from 15-40% based on daily aggregation",
                    "Real-time bidding ensures competitive pricing",
                    "Consumer savings passed through from volume advantages",
                    "Transparent bidding process shows true market rates"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting daily volume bidding: {e}")
        raise HTTPException(status_code=500, detail=f"Volume bidding failed: {str(e)}")

@router.get("/carrier-comparison")
async def get_carrier_comparison(
    origin: str,
    destination: str,
    weight_kg: float,
    volume_cm3: float,
    shipping_service: SEEKERGlobalShippingService = Depends(get_global_shipping_service)
):
    """
    Compare all carriers for a specific shipping route
    """
    try:
        logger.info(f"🏆 Comparing carriers for {origin} → {destination}")
        
        # Get quotes for all service types
        all_carriers = []
        service_types = ['express', 'standard', 'economy', 'ground', 'air']
        
        for service_type in service_types:
            try:
                service_enum = ShippingService(service_type)
                quote = await shipping_service.get_consumer_shipping_quote(
                    origin, destination, weight_kg, volume_cm3, service_enum
                )
                
                for carrier in quote.top_3_carriers:
                    carrier_info = {
                        'service_type': service_type,
                        'carrier_name': carrier['carrier_name'],
                        'rank': carrier['rank'],
                        'final_rate_usd': carrier['final_rate_usd'],
                        'delivery_days': carrier['delivery_days'],
                        'reliability_score': carrier['reliability_score'],
                        'sustainability_score': carrier['sustainability_score'],
                        'consumer_value_score': carrier['consumer_value_score'],
                        'volume_discount_percentage': carrier['volume_discount_percentage']
                    }
                    all_carriers.append(carrier_info)
            except Exception as e:
                logger.warning(f"Error getting quote for {service_type}: {e}")
                continue
        
        # Sort by consumer value score
        all_carriers.sort(key=lambda x: x['consumer_value_score'], reverse=True)
        
        # Group by carrier for summary
        carrier_summary = {}
        for carrier in all_carriers:
            carrier_name = carrier['carrier_name']
            if carrier_name not in carrier_summary:
                carrier_summary[carrier_name] = {
                    'carrier_name': carrier_name,
                    'services_offered': 0,
                    'average_rate_usd': 0,
                    'average_delivery_days': 0,
                    'average_reliability': 0,
                    'average_sustainability': 0,
                    'best_value_score': 0,
                    'total_volume_discount': 0
                }
            
            summary = carrier_summary[carrier_name]
            summary['services_offered'] += 1
            summary['average_rate_usd'] += carrier['final_rate_usd']
            summary['average_delivery_days'] += carrier['delivery_days']
            summary['average_reliability'] += carrier['reliability_score']
            summary['average_sustainability'] += carrier['sustainability_score']
            summary['total_volume_discount'] += carrier['volume_discount_percentage']
            
            if carrier['consumer_value_score'] > summary['best_value_score']:
                summary['best_value_score'] = carrier['consumer_value_score']
        
        # Calculate averages
        for carrier_name, summary in carrier_summary.items():
            services = summary['services_offered']
            summary['average_rate_usd'] = round(summary['average_rate_usd'] / services, 2)
            summary['average_delivery_days'] = round(summary['average_delivery_days'] / services, 1)
            summary['average_reliability'] = round(summary['average_reliability'] / services, 3)
            summary['average_sustainability'] = round(summary['average_sustainability'] / services, 3)
            summary['total_volume_discount'] = round(summary['total_volume_discount'] / services, 1)
        
        # Sort summary by best value score
        carrier_summary_list = list(carrier_summary.values())
        carrier_summary_list.sort(key=lambda x: x['best_value_score'], reverse=True)
        
        return {
            "status": "success",
            "message": f"Carrier comparison completed for {origin} → {destination}",
            "data": {
                "origin": origin,
                "destination": destination,
                "weight_kg": weight_kg,
                "volume_cm3": volume_cm3,
                "total_carriers_compared": len(carrier_summary),
                "total_quotes_generated": len(all_carriers),
                "carrier_summary": carrier_summary_list,
                "detailed_comparison": all_carriers[:20],  # Top 20 results
                "comparison_insights": [
                    "Volume bidding creates 15-40% savings for consumers",
                    "DHL leads in sustainability and reliability scores",
                    "Regional carriers offer best value for local routes",
                    "Express services have highest reliability scores",
                    "Ground shipping provides best sustainability options"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error comparing carriers: {e}")
        raise HTTPException(status_code=500, detail=f"Carrier comparison failed: {str(e)}")

@router.get("/shipping-transparency")
async def get_shipping_transparency_report(
    origin: str,
    destination: str,
    weight_kg: float,
    volume_cm3: float,
    shipping_service: SEEKERGlobalShippingService = Depends(get_global_shipping_service)
):
    """
    Get complete shipping transparency report with cost breakdowns
    """
    try:
        logger.info(f"🔍 Generating shipping transparency report: {origin} → {destination}")
        
        # Get quotes for different service types
        transparency_data = []
        service_types = ['express', 'standard', 'economy']
        
        for service_type in service_types:
            try:
                service_enum = ShippingService(service_type)
                quote = await shipping_service.get_consumer_shipping_quote(
                    origin, destination, weight_kg, volume_cm3, service_enum
                )
                
                for carrier in quote.top_3_carriers:
                    transparency_info = {
                        'service_type': service_type,
                        'carrier_name': carrier['carrier_name'],
                        'rank': carrier['rank'],
                        'final_rate_usd': carrier['final_rate_usd'],
                        'transparency_breakdown': carrier['transparency_breakdown'],
                        'volume_discount_percentage': carrier['volume_discount_percentage'],
                        'reliability_score': carrier['reliability_score'],
                        'sustainability_score': carrier['sustainability_score']
                    }
                    transparency_data.append(transparency_info)
            except Exception as e:
                logger.warning(f"Error getting transparency data for {service_type}: {e}")
                continue
        
        # Calculate transparency metrics
        total_savings = sum(quote.volume_advantage_savings for _ in range(len(transparency_data)))
        avg_transparency_score = np.mean([
            carrier['reliability_score'] * 0.6 + carrier['sustainability_score'] * 0.4 
            for data in transparency_data 
            for carrier in [data]
        ])
        
        return {
            "status": "success",
            "message": f"Shipping transparency report generated for {origin} → {destination}",
            "data": {
                "origin": origin,
                "destination": destination,
                "weight_kg": weight_kg,
                "volume_cm3": volume_cm3,
                "total_volume_savings": round(total_savings, 2),
                "average_transparency_score": round(avg_transparency_score, 3),
                "transparency_rankings": sorted(transparency_data, key=lambda x: x['final_rate_usd']),
                "cost_breakdown_analysis": {
                    "base_shipping_costs": "Direct transportation and handling costs",
                    "volume_discounts": "Savings from daily volume aggregation",
                    "carrier_margins": "Estimated profit margins (typically 10-20%)",
                    "operational_costs": "Fuel, labor, vehicle maintenance (60-70%)",
                    "regulatory_fees": "Government taxes and compliance costs (5-10%)",
                    "fuel_surcharges": "Variable fuel cost adjustments (8-15%)"
                },
                "transparency_insights": [
                    "Complete cost breakdown reveals true pricing structure",
                    "Volume bidding reduces costs by 15-40%",
                    "Carrier margins typically range from 10-20%",
                    "Operational costs represent 60-70% of total price",
                    "Regulatory fees and fuel surcharges add 13-25%"
                ],
                "consumer_empowerment": [
                    "See exactly what you're paying for",
                    "Compare true costs across carriers",
                    "Understand volume discount benefits",
                    "Make informed sustainability choices",
                    "Track real-time pricing transparency"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating transparency report: {e}")
        raise HTTPException(status_code=500, detail=f"Transparency report failed: {str(e)}")

@router.get("/sustainability-comparison")
async def get_sustainability_comparison(
    origin: str,
    destination: str,
    weight_kg: float,
    volume_cm3: float,
    shipping_service: SEEKERGlobalShippingService = Depends(get_global_shipping_service)
):
    """
    Compare carriers based on sustainability and environmental impact
    """
    try:
        logger.info(f"🌱 Generating sustainability comparison: {origin} → {destination}")
        
        # Get sustainability data for all service types
        sustainability_data = []
        service_types = ['express', 'standard', 'economy', 'ground', 'air', 'sea']
        
        for service_type in service_types:
            try:
                service_enum = ShippingService(service_type)
                quote = await shipping_service.get_consumer_shipping_quote(
                    origin, destination, weight_kg, volume_cm3, service_enum
                )
                
                for carrier in quote.sustainability_ranking:
                    sustainability_info = {
                        'service_type': service_type,
                        'carrier_name': carrier['carrier'],
                        'sustainability_score': carrier['sustainability_score'],
                        'carbon_footprint_kg': carrier['carbon_footprint_kg'],
                        'renewable_energy_usage': carrier['renewable_energy_usage'],
                        'eco_friendly_packaging': carrier['eco_friendly_packaging'],
                        'sustainability_initiatives': carrier['sustainability_initiatives']
                    }
                    sustainability_data.append(sustainability_info)
            except Exception as e:
                logger.warning(f"Error getting sustainability data for {service_type}: {e}")
                continue
        
        # Calculate sustainability metrics
        avg_sustainability = np.mean([data['sustainability_score'] for data in sustainability_data])
        avg_carbon_footprint = np.mean([data['carbon_footprint_kg'] for data in sustainability_data])
        avg_renewable_energy = np.mean([data['renewable_energy_usage'] for data in sustainability_data])
        
        # Group by carrier for summary
        carrier_sustainability = {}
        for data in sustainability_data:
            carrier_name = data['carrier_name']
            if carrier_name not in carrier_sustainability:
                carrier_sustainability[carrier_name] = {
                    'carrier_name': carrier_name,
                    'services_analyzed': 0,
                    'average_sustainability_score': 0,
                    'average_carbon_footprint': 0,
                    'average_renewable_energy': 0,
                    'eco_packaging_score': 0,
                    'sustainability_initiatives': []
                }
            
            summary = carrier_sustainability[carrier_name]
            summary['services_analyzed'] += 1
            summary['average_sustainability_score'] += data['sustainability_score']
            summary['average_carbon_footprint'] += data['carbon_footprint_kg']
            summary['average_renewable_energy'] += data['renewable_energy_usage']
            summary['eco_packaging_score'] += data['eco_friendly_packaging']
            
            # Collect unique initiatives
            for initiative in data['sustainability_initiatives']:
                if initiative not in summary['sustainability_initiatives']:
                    summary['sustainability_initiatives'].append(initiative)
        
        # Calculate averages
        for carrier_name, summary in carrier_sustainability.items():
            services = summary['services_analyzed']
            summary['average_sustainability_score'] = round(summary['average_sustainability_score'] / services, 3)
            summary['average_carbon_footprint'] = round(summary['average_carbon_footprint'] / services, 2)
            summary['average_renewable_energy'] = round(summary['average_renewable_energy'] / services, 3)
            summary['eco_packaging_score'] = round(summary['eco_packaging_score'] / services, 3)
        
        # Sort by sustainability score
        carrier_sustainability_list = list(carrier_sustainability.values())
        carrier_sustainability_list.sort(key=lambda x: x['average_sustainability_score'], reverse=True)
        
        return {
            "status": "success",
            "message": f"Sustainability comparison completed for {origin} → {destination}",
            "data": {
                "origin": origin,
                "destination": destination,
                "weight_kg": weight_kg,
                "volume_cm3": volume_cm3,
                "overall_sustainability_metrics": {
                    "average_sustainability_score": round(avg_sustainability, 3),
                    "average_carbon_footprint_kg": round(avg_carbon_footprint, 2),
                    "average_renewable_energy_usage": round(avg_renewable_energy * 100, 1),
                    "total_carriers_analyzed": len(carrier_sustainability)
                },
                "carrier_sustainability_ranking": carrier_sustainability_list,
                "detailed_sustainability_data": sustainability_data,
                "sustainability_insights": [
                    "DHL leads with 85% sustainability score",
                    "Ground shipping has lowest carbon footprint",
                    "Sea freight is most environmentally friendly",
                    "Express services have highest carbon impact",
                    "Renewable energy usage ranges from 15-35%"
                ],
                "environmental_impact_analysis": {
                    "carbon_footprint_ranges": {
                        "express": "8-12 kg CO2",
                        "standard": "5-8 kg CO2", 
                        "economy": "3-6 kg CO2",
                        "ground": "2-4 kg CO2",
                        "air": "8-12 kg CO2",
                        "sea": "1-3 kg CO2"
                    },
                    "sustainability_recommendations": [
                        "Choose ground shipping for lowest environmental impact",
                        "Consider sea freight for non-urgent shipments",
                        "Look for carriers with high renewable energy usage",
                        "Select eco-friendly packaging options",
                        "Support carriers with carbon neutral programs"
                    ]
                },
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error generating sustainability comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Sustainability comparison failed: {str(e)}")

@router.get("/global-shipping-insights")
async def get_global_shipping_insights(
    shipping_service: SEEKERGlobalShippingService = Depends(get_global_shipping_service)
):
    """
    Get comprehensive global shipping market insights
    """
    try:
        logger.info("📊 Generating global shipping insights")
        
        insights = await shipping_service.get_global_shipping_insights()
        
        return {
            "status": "success",
            "message": "Global shipping insights generated",
            "data": insights
        }
    except Exception as e:
        logger.error(f"Error generating global shipping insights: {e}")
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

@router.get("/available-carriers")
async def get_available_carriers():
    """
    Get list of all available shipping carriers
    """
    carriers = [
        {
            "carrier": "FEDEX",
            "name": "Federal Express",
            "regions": ["north_america", "europe", "asia", "australia_oceania"],
            "services": ["express", "standard", "economy", "ground", "air"],
            "reliability_score": 0.95,
            "sustainability_score": 0.78
        },
        {
            "carrier": "UPS",
            "name": "United Parcel Service",
            "regions": ["north_america", "europe", "asia", "south_america"],
            "services": ["express", "standard", "economy", "ground", "air"],
            "reliability_score": 0.93,
            "sustainability_score": 0.82
        },
        {
            "carrier": "DHL",
            "name": "DHL Express",
            "regions": ["north_america", "europe", "asia", "africa", "south_america", "australia_oceania"],
            "services": ["express", "standard", "economy", "ground", "air", "sea"],
            "reliability_score": 0.91,
            "sustainability_score": 0.85
        },
        {
            "carrier": "USPS",
            "name": "United States Postal Service",
            "regions": ["north_america"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.88,
            "sustainability_score": 0.75
        },
        {
            "carrier": "ROYAL_MAIL",
            "name": "Royal Mail",
            "regions": ["europe"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.89,
            "sustainability_score": 0.80
        },
        {
            "carrier": "DEUTSCHE_POST",
            "name": "Deutsche Post",
            "regions": ["europe"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.90,
            "sustainability_score": 0.83
        },
        {
            "carrier": "JAPAN_POST",
            "name": "Japan Post",
            "regions": ["asia"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.92,
            "sustainability_score": 0.79
        },
        {
            "carrier": "CHINA_POST",
            "name": "China Post",
            "regions": ["asia"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.87,
            "sustainability_score": 0.72
        },
        {
            "carrier": "AUSTRALIA_POST",
            "name": "Australia Post",
            "regions": ["australia_oceania"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.89,
            "sustainability_score": 0.81
        },
        {
            "carrier": "CANADA_POST",
            "name": "Canada Post",
            "regions": ["north_america"],
            "services": ["express", "standard", "economy", "ground"],
            "reliability_score": 0.91,
            "sustainability_score": 0.84
        },
        {
            "carrier": "REGIONAL_CARRIERS",
            "name": "Regional Carriers",
            "regions": ["africa", "south_america", "antarctica"],
            "services": ["standard", "economy", "ground"],
            "reliability_score": 0.85,
            "sustainability_score": 0.70
        }
    ]
    
    return {
        "status": "success",
        "message": "Available carriers retrieved",
        "data": {
            "carriers": carriers,
            "total_carriers": len(carriers),
            "continents_covered": 7,
            "service_types": ["express", "standard", "economy", "ground", "air", "sea"],
            "timestamp": datetime.now().isoformat()
        }
    }

@router.get("/health")
async def health_check():
    """
    Health check for Global Shipping Marketplace service
    """
    return {
        "status": "healthy",
        "service": "Global Shipping Marketplace",
        "features": [
            "Daily Volume Bidding System",
            "Consumer Shipping Transparency",
            "Carrier Competition Platform",
            "Sustainability Comparison",
            "Global Logistics Optimization"
        ],
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    } 