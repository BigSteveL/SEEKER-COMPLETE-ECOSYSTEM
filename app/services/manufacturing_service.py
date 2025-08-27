"""
SEEKER Manufacturing Service
AI-assisted product prototyping and rapid iteration
On-demand global manufacturing connections
AI-facilitated mass production scaling
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid
from collections import defaultdict

from app.services.classification_engine import TaskClassificationEngine as ClassificationEngine

logger = logging.getLogger(__name__)

class ManufacturingService:
    def __init__(self):
        self.classification_engine = ClassificationEngine()
        self.manufacturing_jobs = {}
        self.manufacturing_partners = {}
        self.quality_metrics = defaultdict(list)
        self.performance_data = defaultdict(list)
        
        # Initialize manufacturing partners
        self.initialize_manufacturing_partners()
        
        # Background tasks will be started when needed
        # asyncio.create_task(self._monitor_manufacturing_jobs())
        # asyncio.create_task(self._update_performance_metrics())

    def initialize_manufacturing_partners(self):
        """Initialize global manufacturing partners"""
        self.manufacturing_partners = {
            "shapeways": {
                "name": "Shapeways",
                "capabilities": ["3D Printing", "Materials", "Finishing"],
                "locations": ["Netherlands", "USA", "Germany"],
                "materials": ["Plastic", "Metal", "Ceramic", "Glass"],
                "quality_rating": 4.8,
                "avg_lead_time": 7,
                "cost_factor": 1.2
            },
            "3dhubs": {
                "name": "3D Hubs",
                "capabilities": ["Local Manufacturing", "Rapid Prototyping", "Production"],
                "locations": ["Global Network"],
                "materials": ["PLA", "ABS", "PETG", "TPU", "Metal"],
                "quality_rating": 4.5,
                "avg_lead_time": 5,
                "cost_factor": 1.0
            },
            "protolabs": {
                "name": "Protolabs",
                "capabilities": ["Injection Molding", "CNC Machining", "3D Printing"],
                "locations": ["USA", "Europe", "Asia"],
                "materials": ["Engineering Plastics", "Metals", "Elastomers"],
                "quality_rating": 4.9,
                "avg_lead_time": 3,
                "cost_factor": 1.5
            },
            "xometry": {
                "name": "Xometry",
                "capabilities": ["CNC Machining", "3D Printing", "Sheet Metal", "Injection Molding"],
                "locations": ["USA", "Europe"],
                "materials": ["Aluminum", "Steel", "Plastic", "Titanium"],
                "quality_rating": 4.7,
                "avg_lead_time": 4,
                "cost_factor": 1.3
            }
        }

    async def optimize_design_for_manufacturing(
        self, 
        design_data: Dict[str, Any], 
        manufacturing_type: str,
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AI-assisted design optimization for manufacturing
        """
        try:
            logger.info(f"Optimizing design for {manufacturing_type} manufacturing")
            
            # Analyze design for manufacturing constraints
            constraints = await self._analyze_manufacturing_constraints(
                design_data, 
                manufacturing_type
            )
            
            # Generate optimization recommendations
            recommendations = await self._generate_optimization_recommendations(
                design_data, 
                constraints, 
                requirements
            )
            
            # Calculate potential improvements
            improvements = await self._calculate_improvements(
                design_data, 
                recommendations
            )
            
            return {
                "original_design": design_data,
                "constraints": constraints,
                "recommendations": recommendations,
                "improvements": improvements,
                "cost_savings": improvements.get("cost_savings", 0),
                "time_savings": improvements.get("time_savings", 0),
                "quality_improvements": improvements.get("quality_improvements", 0)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing design for manufacturing: {e}")
            raise

    async def _analyze_manufacturing_constraints(
        self, 
        design_data: Dict[str, Any], 
        manufacturing_type: str
    ) -> Dict[str, Any]:
        """Analyze design for manufacturing constraints"""
        
        constraints = {
            "dimensional_limits": {},
            "material_constraints": [],
            "process_limitations": [],
            "cost_factors": {},
            "quality_considerations": []
        }
        
        # Analyze dimensional constraints
        dimensions = design_data.get("dimensions", {})
        if manufacturing_type == "3d_printing":
            constraints["dimensional_limits"] = {
                "max_size": {"x": 300, "y": 300, "z": 300},  # mm
                "min_wall_thickness": 0.8,  # mm
                "max_overhang_angle": 45  # degrees
            }
        elif manufacturing_type == "cnc_machining":
            constraints["dimensional_limits"] = {
                "max_size": {"x": 500, "y": 500, "z": 500},  # mm
                "min_feature_size": 0.5,  # mm
                "tool_access_requirements": True
            }
        elif manufacturing_type == "injection_molding":
            constraints["dimensional_limits"] = {
                "max_size": {"x": 1000, "y": 1000, "z": 1000},  # mm
                "min_wall_thickness": 1.0,  # mm
                "draft_angle_required": 2  # degrees
            }
        
        # Analyze material constraints
        material = design_data.get("material", "PLA")
        if manufacturing_type == "3d_printing":
            constraints["material_constraints"] = [
                "Material must be compatible with 3D printing process",
                "Consider layer adhesion and support structures",
                "Account for thermal expansion and warping"
            ]
        elif manufacturing_type == "cnc_machining":
            constraints["material_constraints"] = [
                "Material must be machinable",
                "Consider tool wear and cutting parameters",
                "Account for material hardness and toughness"
            ]
        
        # Analyze process limitations
        if manufacturing_type == "3d_printing":
            constraints["process_limitations"] = [
                "Layer-by-layer build process",
                "Support structures required for overhangs",
                "Post-processing may be needed"
            ]
        elif manufacturing_type == "cnc_machining":
            constraints["process_limitations"] = [
                "Tool access limitations",
                "Setup time for different operations",
                "Material waste from subtractive process"
            ]
        
        return constraints

    async def _generate_optimization_recommendations(
        self, 
        design_data: Dict[str, Any], 
        constraints: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate AI-powered optimization recommendations"""
        
        recommendations = []
        
        # Dimensional optimization
        dimensions = design_data.get("dimensions", {})
        dim_limits = constraints.get("dimensional_limits", {})
        
        if "max_size" in dim_limits:
            for axis, max_size in dim_limits["max_size"].items():
                if dimensions.get(axis, 0) > max_size:
                    recommendations.append({
                        "type": "dimensional_optimization",
                        "priority": "high",
                        "description": f"Reduce {axis} dimension to fit within {max_size}mm limit",
                        "estimated_impact": "cost_reduction",
                        "implementation_effort": "medium"
                    })
        
        # Material optimization
        current_material = design_data.get("material", "PLA")
        if requirements.get("cost_optimization"):
            recommendations.append({
                "type": "material_optimization",
                "priority": "medium",
                "description": f"Consider alternative materials for cost reduction",
                "suggested_materials": ["PLA", "ABS", "PETG"],
                "estimated_impact": "cost_reduction",
                "implementation_effort": "low"
            })
        
        # Process optimization
        if design_data.get("complexity") == "high":
            recommendations.append({
                "type": "process_optimization",
                "priority": "high",
                "description": "Simplify design for easier manufacturing",
                "suggestions": [
                    "Reduce number of complex features",
                    "Increase wall thickness for better printability",
                    "Add fillets to sharp corners"
                ],
                "estimated_impact": "quality_improvement",
                "implementation_effort": "high"
            })
        
        # Quality optimization
        if requirements.get("quality_priority"):
            recommendations.append({
                "type": "quality_optimization",
                "priority": "high",
                "description": "Optimize for maximum quality",
                "suggestions": [
                    "Use higher resolution settings",
                    "Implement proper support structures",
                    "Consider post-processing options"
                ],
                "estimated_impact": "quality_improvement",
                "implementation_effort": "medium"
            })
        
        return recommendations

    async def _calculate_improvements(
        self, 
        design_data: Dict[str, Any], 
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate potential improvements from recommendations"""
        
        improvements = {
            "cost_savings": 0,
            "time_savings": 0,
            "quality_improvements": 0
        }
        
        for rec in recommendations:
            if rec["type"] == "dimensional_optimization":
                improvements["cost_savings"] += 15  # 15% cost reduction
                improvements["time_savings"] += 20   # 20% time reduction
            elif rec["type"] == "material_optimization":
                improvements["cost_savings"] += 10   # 10% cost reduction
            elif rec["type"] == "process_optimization":
                improvements["quality_improvements"] += 25  # 25% quality improvement
                improvements["time_savings"] += 15          # 15% time reduction
            elif rec["type"] == "quality_optimization":
                improvements["quality_improvements"] += 30  # 30% quality improvement
        
        return improvements

    async def find_optimal_manufacturing_connections(
        self, 
        design_data: Dict[str, Any], 
        manufacturing_type: str,
        budget: str,
        timeline: str
    ) -> List[Dict[str, Any]]:
        """
        Find optimal manufacturing connections based on requirements
        """
        try:
            logger.info(f"Finding optimal manufacturing connections for {manufacturing_type}")
            
            connections = []
            
            for partner_id, partner in self.manufacturing_partners.items():
                # Check if partner supports the manufacturing type
                if manufacturing_type in partner["capabilities"]:
                    # Calculate connection score
                    score = await self._calculate_connection_score(
                        partner, 
                        design_data, 
                        budget, 
                        timeline
                    )
                    
                    connection = {
                        "partner_id": partner_id,
                        "name": partner["name"],
                        "capabilities": partner["capabilities"],
                        "locations": partner["locations"],
                        "materials": partner["materials"],
                        "quality_rating": partner["quality_rating"],
                        "avg_lead_time": partner["avg_lead_time"],
                        "cost_factor": partner["cost_factor"],
                        "score": score,
                        "available": True
                    }
                    
                    connections.append(connection)
            
            # Sort by score (highest first)
            connections.sort(key=lambda x: x["score"], reverse=True)
            
            return connections
            
        except Exception as e:
            logger.error(f"Error finding manufacturing connections: {e}")
            raise

    async def _calculate_connection_score(
        self, 
        partner: Dict[str, Any], 
        design_data: Dict[str, Any], 
        budget: str, 
        timeline: str
    ) -> float:
        """Calculate connection score based on requirements"""
        
        score = 0.0
        
        # Quality factor (30% weight)
        quality_score = partner["quality_rating"] / 5.0
        score += quality_score * 0.3
        
        # Cost factor (25% weight)
        cost_score = self._calculate_cost_score(partner["cost_factor"], budget)
        score += cost_score * 0.25
        
        # Speed factor (25% weight)
        speed_score = self._calculate_speed_score(partner["avg_lead_time"], timeline)
        score += speed_score * 0.25
        
        # Capability factor (20% weight)
        capability_score = len(partner["capabilities"]) / 10.0  # Normalize to 0-1
        score += capability_score * 0.2
        
        return score

    def _calculate_cost_score(self, cost_factor: float, budget: str) -> float:
        """Calculate cost score based on budget requirements"""
        budget_factors = {
            "low": 1.0,
            "medium": 0.7,
            "high": 0.4
        }
        
        budget_factor = budget_factors.get(budget, 0.7)
        return max(0, 1 - (cost_factor - 1) * budget_factor)

    def _calculate_speed_score(self, avg_lead_time: int, timeline: str) -> float:
        """Calculate speed score based on timeline requirements"""
        timeline_factors = {
            "urgent": 1.0,
            "normal": 0.7,
            "flexible": 0.4
        }
        
        timeline_factor = timeline_factors.get(timeline, 0.7)
        return max(0, 1 - (avg_lead_time / 10) * timeline_factor)

    async def create_manufacturing_job(
        self, 
        design_data: Dict[str, Any], 
        manufacturing_type: str,
        priority: str,
        budget: str
    ) -> Dict[str, Any]:
        """
        Create a new manufacturing job
        """
        try:
            job_id = str(uuid.uuid4())
            
            # Find optimal manufacturing partner
            connections = await self.find_optimal_manufacturing_connections(
                design_data, 
                manufacturing_type, 
                budget, 
                "normal"
            )
            
            if not connections:
                raise Exception("No suitable manufacturing partners found")
            
            optimal_partner = connections[0]
            
            # Calculate estimated cost and completion time
            estimated_cost = await self._calculate_job_cost(
                design_data, 
                optimal_partner, 
                manufacturing_type
            )
            
            estimated_completion = datetime.utcnow() + timedelta(
                days=optimal_partner["avg_lead_time"]
            )
            
            # Create job record
            job = {
                "job_id": job_id,
                "design_data": design_data,
                "manufacturing_type": manufacturing_type,
                "priority": priority,
                "budget": budget,
                "status": "submitted",
                "submitted_at": datetime.utcnow(),
                "estimated_completion": estimated_completion,
                "estimated_cost": estimated_cost,
                "manufacturing_partner": optimal_partner["partner_id"],
                "partner_name": optimal_partner["name"],
                "updates": []
            }
            
            self.manufacturing_jobs[job_id] = job
            
            logger.info(f"Created manufacturing job {job_id} with partner {optimal_partner['name']}")
            
            return job
            
        except Exception as e:
            logger.error(f"Error creating manufacturing job: {e}")
            raise

    async def _calculate_job_cost(
        self, 
        design_data: Dict[str, Any], 
        partner: Dict[str, Any], 
        manufacturing_type: str
    ) -> float:
        """Calculate estimated job cost"""
        
        base_cost = 50  # Base cost for small job
        
        # Material cost
        material_cost = self._get_material_cost(design_data.get("material", "PLA"))
        
        # Complexity multiplier
        complexity = design_data.get("complexity", "medium")
        complexity_multipliers = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.5
        }
        complexity_multiplier = complexity_multipliers.get(complexity, 1.5)
        
        # Quantity multiplier
        quantity = design_data.get("quantity", 1)
        quantity_multiplier = 1 + (quantity - 1) * 0.8  # Bulk discount
        
        # Partner cost factor
        partner_cost_factor = partner.get("cost_factor", 1.0)
        
        total_cost = (base_cost + material_cost) * complexity_multiplier * quantity_multiplier * partner_cost_factor
        
        return round(total_cost, 2)

    def _get_material_cost(self, material: str) -> float:
        """Get material cost per unit"""
        material_costs = {
            "PLA": 20,
            "ABS": 25,
            "PETG": 30,
            "TPU": 40,
            "Carbon Fiber": 200,
            "Titanium": 500
        }
        return material_costs.get(material, 25)

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get manufacturing job status"""
        return self.manufacturing_jobs.get(job_id)

    async def update_job_status(self, job_id: str, status: str, timestamp: str = None):
        """Update manufacturing job status"""
        if job_id in self.manufacturing_jobs:
            job = self.manufacturing_jobs[job_id]
            job["status"] = status
            
            update = {
                "status": status,
                "timestamp": timestamp or datetime.utcnow().isoformat(),
                "message": self._get_status_message(status)
            }
            
            job["updates"].append(update)
            
            logger.info(f"Updated job {job_id} status to {status}")

    def _get_status_message(self, status: str) -> str:
        """Get human-readable status message"""
        messages = {
            "submitted": "Job submitted to manufacturing partner",
            "processing": "Design is being processed and optimized",
            "manufacturing": "Product is being manufactured",
            "quality_check": "Quality assurance and testing in progress",
            "shipping": "Product is being prepared for shipping",
            "completed": "Manufacturing job completed successfully",
            "failed": "Manufacturing job failed"
        }
        return messages.get(status, "Unknown status")

    async def perform_quality_check(self, job_id: str, part_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform quality check on manufactured part
        """
        try:
            logger.info(f"Performing quality check for job {job_id}")
            
            # Simulate quality check
            quality_metrics = {
                "dimensional_accuracy": await self._check_dimensional_accuracy(part_data),
                "surface_finish": await self._check_surface_finish(part_data),
                "material_properties": await self._check_material_properties(part_data),
                "structural_integrity": await self._check_structural_integrity(part_data)
            }
            
            # Calculate overall score
            overall_score = self._calculate_overall_quality_score(quality_metrics)
            
            # Generate recommendations
            recommendations = self._generate_quality_recommendations(quality_metrics)
            
            result = {
                "job_id": job_id,
                "quality_metrics": quality_metrics,
                "overall_score": overall_score,
                "pass_fail": overall_score >= 0.8,
                "recommendations": recommendations,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store quality metrics
            self.quality_metrics[job_id].append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error performing quality check: {e}")
            raise

    async def _check_dimensional_accuracy(self, part_data: Dict[str, Any]) -> float:
        """Check dimensional accuracy"""
        # Simulate dimensional accuracy check
        tolerance = 0.1  # mm
        deviation = (part_data.get("measured_dimensions", {}) or {}).get("max_deviation", 0.05)
        return max(0, 1 - (deviation / tolerance))

    async def _check_surface_finish(self, part_data: Dict[str, Any]) -> float:
        """Check surface finish"""
        # Simulate surface finish check
        roughness = part_data.get("surface_roughness", 2.5)  # Ra in micrometers
        target_roughness = 3.2  # Target Ra
        return max(0, 1 - (roughness / target_roughness))

    async def _check_material_properties(self, part_data: Dict[str, Any]) -> float:
        """Check material properties"""
        # Simulate material properties check
        strength_ratio = part_data.get("strength_ratio", 0.95)  # 95% of expected
        density_ratio = part_data.get("density_ratio", 0.98)    # 98% of expected
        return (strength_ratio + density_ratio) / 2

    async def _check_structural_integrity(self, part_data: Dict[str, Any]) -> float:
        """Check structural integrity"""
        # Simulate structural integrity check
        return part_data.get("structural_integrity", 0.92)  # 92% integrity

    def _calculate_overall_quality_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall quality score"""
        weights = {
            "dimensional_accuracy": 0.3,
            "surface_finish": 0.2,
            "material_properties": 0.3,
            "structural_integrity": 0.2
        }
        
        return sum(metrics[metric] * weights[metric] for metric in weights)

    def _generate_quality_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        if metrics["dimensional_accuracy"] < 0.8:
            recommendations.append("Adjust manufacturing parameters for better dimensional accuracy")
        
        if metrics["surface_finish"] < 0.7:
            recommendations.append("Consider post-processing for improved surface finish")
        
        if metrics["material_properties"] < 0.8:
            recommendations.append("Verify material selection and processing parameters")
        
        if metrics["structural_integrity"] < 0.9:
            recommendations.append("Review design for structural optimization")
        
        return recommendations

    async def get_available_materials(self) -> List[Dict[str, Any]]:
        """Get list of available manufacturing materials"""
        return [
            {"name": "PLA", "cost": "low", "strength": "medium", "weight": "medium", "availability": "high"},
            {"name": "ABS", "cost": "low", "strength": "high", "weight": "medium", "availability": "high"},
            {"name": "PETG", "cost": "medium", "strength": "high", "weight": "medium", "availability": "high"},
            {"name": "TPU", "cost": "medium", "strength": "medium", "weight": "light", "availability": "medium"},
            {"name": "Carbon Fiber", "cost": "high", "strength": "high", "weight": "light", "availability": "medium"},
            {"name": "Titanium", "cost": "high", "strength": "high", "weight": "light", "availability": "low"}
        ]

    async def get_manufacturing_capabilities(self) -> List[Dict[str, Any]]:
        """Get available manufacturing capabilities"""
        return [
            {"name": "3D Printing", "description": "Additive manufacturing for rapid prototyping", "materials": ["PLA", "ABS", "PETG", "TPU"]},
            {"name": "CNC Machining", "description": "Precision subtractive manufacturing", "materials": ["Aluminum", "Steel", "Plastic", "Titanium"]},
            {"name": "Injection Molding", "description": "High-volume production molding", "materials": ["Engineering Plastics", "Elastomers"]},
            {"name": "Sheet Metal", "description": "Metal forming and fabrication", "materials": ["Aluminum", "Steel", "Stainless Steel"]}
        ]

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get manufacturing performance metrics"""
        total_jobs = len(self.manufacturing_jobs)
        completed_jobs = len([j for j in self.manufacturing_jobs.values() if j["status"] == "completed"])
        failed_jobs = len([j for j in self.manufacturing_jobs.values() if j["status"] == "failed"])
        
        avg_quality_score = 0
        if self.quality_metrics:
            all_scores = [metric["overall_score"] for metrics in self.quality_metrics.values() for metric in metrics]
            avg_quality_score = sum(all_scores) / len(all_scores) if all_scores else 0
        
        return {
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "failed_jobs": failed_jobs,
            "success_rate": (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            "average_quality_score": round(avg_quality_score, 2),
            "active_partners": len(self.manufacturing_partners),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def health_check(self) -> Dict[str, Any]:
        """Health check for manufacturing services"""
        try:
            # Check manufacturing partners
            partner_status = {}
            for partner_id, partner in self.manufacturing_partners.items():
                partner_status[partner_id] = {
                    "name": partner["name"],
                    "status": "available",
                    "capabilities": partner["capabilities"]
                }
            
            # Check active jobs
            active_jobs = len([j for j in self.manufacturing_jobs.values() if j["status"] in ["submitted", "processing", "manufacturing"]])
            
            return {
                "status": "healthy",
                "partners": partner_status,
                "active_jobs": active_jobs,
                "total_jobs": len(self.manufacturing_jobs)
            }
            
        except Exception as e:
            logger.error(f"Manufacturing health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

    async def _monitor_manufacturing_jobs(self):
        """Background task to monitor manufacturing jobs"""
        while True:
            try:
                for job_id, job in self.manufacturing_jobs.items():
                    if job["status"] in ["submitted", "processing", "manufacturing"]:
                        # Simulate job progress
                        await self._simulate_job_progress(job_id)
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error monitoring manufacturing jobs: {e}")
                await asyncio.sleep(60)

    async def _simulate_job_progress(self, job_id: str):
        """Simulate manufacturing job progress"""
        job = self.manufacturing_jobs[job_id]
        
        # Simulate progress based on time elapsed
        elapsed = datetime.utcnow() - job["submitted_at"]
        elapsed_hours = elapsed.total_seconds() / 3600
        
        # Update status based on elapsed time
        if elapsed_hours < 1 and job["status"] == "submitted":
            await self.update_job_status(job_id, "processing")
        elif elapsed_hours < 4 and job["status"] == "processing":
            await self.update_job_status(job_id, "manufacturing")
        elif elapsed_hours < 8 and job["status"] == "manufacturing":
            await self.update_job_status(job_id, "quality_check")
        elif elapsed_hours < 10 and job["status"] == "quality_check":
            await self.update_job_status(job_id, "shipping")
        elif elapsed_hours < 12 and job["status"] == "shipping":
            await self.update_job_status(job_id, "completed")

    async def _update_performance_metrics(self):
        """Background task to update performance metrics"""
        while True:
            try:
                metrics = await self.get_performance_metrics()
                self.performance_data[datetime.utcnow().isoformat()] = metrics
                
                # Keep only last 100 entries
                if len(self.performance_data) > 100:
                    oldest_key = min(self.performance_data.keys())
                    del self.performance_data[oldest_key]
                
                await asyncio.sleep(300)  # Update every 5 minutes
                
            except Exception as e:
                logger.error(f"Error updating performance metrics: {e}")
                await asyncio.sleep(300)

    async def get_recent_updates(self) -> List[Dict[str, Any]]:
        """Get recent manufacturing updates for WebSocket"""
        updates = []
        
        for job_id, job in self.manufacturing_jobs.items():
            if job["updates"]:
                latest_update = job["updates"][-1]
                updates.append({
                    "job_id": job_id,
                    "status": latest_update["status"],
                    "message": latest_update["message"],
                    "timestamp": latest_update["timestamp"]
                })
        
        return updates[-10:]  # Return last 10 updates 