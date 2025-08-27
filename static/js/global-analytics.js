/**
 * SEEKER Global Analytics Validation System
 * Frontend module for global market intelligence and supplier analysis
 */

class SEEKERGlobalAnalytics {
    constructor() {
        this.currentIndustry = '';
        this.currentProductCategory = '';
        this.heatmapChart = null;
        this.reliabilityChart = null;
        this.isAnalyzing = false;
        
        this.industries = [
            'Electronics', 'Automotive', 'Aerospace', 'Healthcare', 
            'Construction', 'Energy', 'Textiles', 'Food & Beverage',
            'Chemicals', 'Pharmaceuticals', 'Machinery', 'Telecommunications'
        ];
        
        this.productCategories = [
            'Components', 'Raw Materials', 'Finished Goods', 'Equipment',
            'Services', 'Software', 'Hardware', 'Consumables'
        ];
        
        this.init();
    }
    
    init() {
        console.log('🌍 SEEKER Global Analytics System initialized');
        this.setupEventListeners();
        this.loadInitialData();
    }
    
    setupEventListeners() {
        // Industry selection
        const industrySelect = document.getElementById('industrySelect');
        if (industrySelect) {
            industrySelect.addEventListener('change', (e) => {
                this.currentIndustry = e.target.value;
                this.onIndustryChange();
            });
        }
        
        // Product category selection
        const productCategorySelect = document.getElementById('productCategorySelect');
        if (productCategorySelect) {
            productCategorySelect.addEventListener('change', (e) => {
                this.currentProductCategory = e.target.value;
                this.onProductCategoryChange();
            });
        }
        
        // Analysis button
        const analyzeBtn = document.getElementById('analyzeMarketBtn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.analyzeMarket());
        }
        
        // Refresh data button
        const refreshBtn = document.getElementById('refreshDataBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshMarketData());
        }
        
        // Export button
        const exportBtn = document.getElementById('exportDataBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportAnalysisData());
        }
    }
    
    loadInitialData() {
        this.populateIndustrySelect();
        this.populateProductCategorySelect();
        this.loadContinentsData();
        this.loadDataSourcesInfo();
    }
    
    populateIndustrySelect() {
        const industrySelect = document.getElementById('industrySelect');
        if (!industrySelect) return;
        
        industrySelect.innerHTML = '<option value="">Select Industry</option>';
        this.industries.forEach(industry => {
            const option = document.createElement('option');
            option.value = industry;
            option.textContent = industry;
            industrySelect.appendChild(option);
        });
    }
    
    populateProductCategorySelect() {
        const productCategorySelect = document.getElementById('productCategorySelect');
        if (!productCategorySelect) return;
        
        productCategorySelect.innerHTML = '<option value="">Select Product Category</option>';
        this.productCategories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            productCategorySelect.appendChild(option);
        });
    }
    
    async loadContinentsData() {
        try {
            const response = await fetch('/api/v1/global-analytics/continents');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayContinentsInfo(data.data.continents);
            }
        } catch (error) {
            console.error('Error loading continents data:', error);
        }
    }
    
    async loadDataSourcesInfo() {
        try {
            const response = await fetch('/api/v1/global-analytics/data-sources');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayDataSourcesInfo(data.data.data_sources);
            }
        } catch (error) {
            console.error('Error loading data sources info:', error);
        }
    }
    
    displayContinentsInfo(continents) {
        const continentsContainer = document.getElementById('continentsInfo');
        if (!continentsContainer) return;
        
        continentsContainer.innerHTML = '';
        continents.forEach(continent => {
            const continentCard = document.createElement('div');
            continentCard.className = 'continent-card';
            continentCard.innerHTML = `
                <div class="continent-header">
                    <h6>${continent.name}</h6>
                    <span class="continent-id">${continent.id}</span>
                </div>
                <p class="continent-description">${continent.description}</p>
            `;
            continentsContainer.appendChild(continentCard);
        });
    }
    
    displayDataSourcesInfo(dataSources) {
        const sourcesContainer = document.getElementById('dataSourcesInfo');
        if (!sourcesContainer) return;
        
        sourcesContainer.innerHTML = '';
        dataSources.forEach(source => {
            const sourceCard = document.createElement('div');
            sourceCard.className = 'data-source-card';
            sourceCard.innerHTML = `
                <div class="source-header">
                    <h6>${source.name}</h6>
                    <span class="source-id">${source.id}</span>
                </div>
                <p class="source-description">${source.description}</p>
            `;
            sourcesContainer.appendChild(sourceCard);
        });
    }
    
    onIndustryChange() {
        console.log('🏭 Industry changed to:', this.currentIndustry);
        this.updateAnalysisStatus();
    }
    
    onProductCategoryChange() {
        console.log('📦 Product category changed to:', this.currentProductCategory);
        this.updateAnalysisStatus();
    }
    
    updateAnalysisStatus() {
        const analyzeBtn = document.getElementById('analyzeMarketBtn');
        if (!analyzeBtn) return;
        
        if (this.currentIndustry && this.currentProductCategory) {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = `Analyze ${this.currentIndustry} - ${this.currentProductCategory}`;
        } else {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Select Industry and Product Category';
        }
    }
    
    async analyzeMarket() {
        if (!this.currentIndustry || !this.currentProductCategory) {
            this.showNotification('Please select both industry and product category', 'warning');
            return;
        }
        
        if (this.isAnalyzing) {
            this.showNotification('Analysis already in progress...', 'info');
            return;
        }
        
        this.isAnalyzing = true;
        this.showAnalysisProgress();
        
        try {
            console.log('🔍 Starting global market analysis...');
            
            // Perform market analysis
            const analysisResult = await this.performMarketAnalysis();
            
            // Generate visualizations
            await this.generateVisualizations();
            
            // Display results
            this.displayAnalysisResults(analysisResult);
            
            this.showNotification('Global market analysis completed successfully!', 'success');
            
        } catch (error) {
            console.error('Error in market analysis:', error);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.isAnalyzing = false;
            this.hideAnalysisProgress();
        }
    }
    
    async performMarketAnalysis() {
        const response = await fetch('/api/v1/global-analytics/analyze-market', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                industry: this.currentIndustry,
                product_category: this.currentProductCategory
            })
        });
        
        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        return data.data;
    }
    
    async generateVisualizations() {
        // Generate heatmap
        await this.generateGlobalHeatmap();
        
        // Generate supplier reliability chart
        await this.generateSupplierReliabilityChart();
        
        // Generate market summary
        await this.generateMarketSummary();
    }
    
    async generateGlobalHeatmap() {
        try {
            const response = await fetch(`/api/v1/global-analytics/heatmap-data?industry=${this.currentIndustry}&product_category=${this.currentProductCategory}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.createHeatmapVisualization(data.data);
            }
        } catch (error) {
            console.error('Error generating heatmap:', error);
        }
    }
    
    async generateSupplierReliabilityChart() {
        try {
            const response = await fetch(`/api/v1/global-analytics/supplier-reliability?industry=${this.currentIndustry}&product_category=${this.currentProductCategory}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.createReliabilityChart(data.data.suppliers);
            }
        } catch (error) {
            console.error('Error generating reliability chart:', error);
        }
    }
    
    async generateMarketSummary() {
        try {
            const response = await fetch(`/api/v1/global-analytics/market-summary?industry=${this.currentIndustry}&product_category=${this.currentProductCategory}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayMarketSummary(data.data);
            }
        } catch (error) {
            console.error('Error generating market summary:', error);
        }
    }
    
    createHeatmapVisualization(heatmapData) {
        const heatmapContainer = document.getElementById('globalHeatmap');
        if (!heatmapContainer) return;
        
        // Clear existing chart
        if (this.heatmapChart) {
            this.heatmapChart.destroy();
        }
        
        const ctx = document.createElement('canvas');
        heatmapContainer.innerHTML = '';
        heatmapContainer.appendChild(ctx);
        
        // Prepare data for heatmap
        const continents = Object.keys(heatmapData.heatmap_data);
        const metrics = ['supplier_count', 'avg_price', 'avg_quality', 'avg_reliability'];
        
        const datasets = metrics.map((metric, index) => ({
            label: metric.replace('_', ' ').toUpperCase(),
            data: continents.map(continent => heatmapData.heatmap_data[continent][metric] || 0),
            backgroundColor: this.getColorForMetric(metric),
            borderColor: this.getColorForMetric(metric),
            borderWidth: 1
        }));
        
        this.heatmapChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: continents.map(c => c.replace('_', ' ').toUpperCase()),
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: `Global Market Heatmap - ${this.currentIndustry} - ${this.currentProductCategory}`
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    createReliabilityChart(suppliers) {
        const reliabilityContainer = document.getElementById('supplierReliability');
        if (!reliabilityContainer) return;
        
        // Clear existing chart
        if (this.reliabilityChart) {
            this.reliabilityChart.destroy();
        }
        
        const ctx = document.createElement('canvas');
        reliabilityContainer.innerHTML = '';
        reliabilityContainer.appendChild(ctx);
        
        // Prepare data for reliability chart
        const topSuppliers = suppliers.slice(0, 10); // Top 10 suppliers
        const labels = topSuppliers.map(s => s.supplier_name.substring(0, 20) + '...');
        const reliabilityScores = topSuppliers.map(s => s.reliability_score * 100);
        const qualityScores = topSuppliers.map(s => s.quality_score * 100);
        
        this.reliabilityChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Reliability Score (%)',
                        data: reliabilityScores,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2
                    },
                    {
                        label: 'Quality Score (%)',
                        data: qualityScores,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: `Top Supplier Reliability Analysis - ${this.currentIndustry}`
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
    
    displayMarketSummary(summary) {
        const summaryContainer = document.getElementById('marketSummary');
        if (!summaryContainer) return;
        
        summaryContainer.innerHTML = `
            <div class="market-summary-card">
                <h5>Market Summary</h5>
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="summary-label">Market Penetration</span>
                        <span class="summary-value">${summary.market_penetration}%</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Opportunity Score</span>
                        <span class="summary-value">${summary.opportunity_score}%</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Total Suppliers</span>
                        <span class="summary-value">${summary.total_suppliers}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Continents Covered</span>
                        <span class="summary-value">${summary.continents_covered}/7</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Average Price</span>
                        <span class="summary-value">$${summary.average_price_usd}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Compliance Rate</span>
                        <span class="summary-value">${summary.compliance_rate.toFixed(1)}%</span>
                    </div>
                </div>
                <div class="top-suppliers">
                    <h6>Top Suppliers by Efficiency:</h6>
                    <ul>
                        ${summary.top_suppliers.map(supplier => `<li>${supplier}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }
    
    displayAnalysisResults(results) {
        const resultsContainer = document.getElementById('analysisResults');
        if (!resultsContainer) return;
        
        resultsContainer.innerHTML = `
            <div class="analysis-results">
                <h4>Global Market Analysis Results</h4>
                <div class="results-grid">
                    <div class="result-card">
                        <h6>Market Penetration</h6>
                        <div class="result-value">${results.market_penetration}%</div>
                        <p>Global market coverage and supplier density</p>
                    </div>
                    <div class="result-card">
                        <h6>Opportunity Score</h6>
                        <div class="result-value">${results.opportunity_score}%</div>
                        <p>Overall market opportunity assessment</p>
                    </div>
                    <div class="result-card">
                        <h6>Supply Chain Routes</h6>
                        <div class="result-value">${results.supply_chain_routes.length}</div>
                        <p>Optimized supply chain pathways identified</p>
                    </div>
                    <div class="result-card">
                        <h6>Compliance Status</h6>
                        <div class="result-value">${Object.values(results.compliance_status).filter(Boolean).length}/${Object.keys(results.compliance_status).length}</div>
                        <p>Regulatory compliance across regions</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    async refreshMarketData() {
        if (!this.currentIndustry || !this.currentProductCategory) {
            this.showNotification('Please select industry and product category first', 'warning');
            return;
        }
        
        try {
            this.showNotification('Refreshing market data...', 'info');
            
            const response = await fetch('/api/v1/global-analytics/collect-market-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    industry: this.currentIndustry,
                    product_category: this.currentProductCategory
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.showNotification(`Refreshed ${data.data.total_records} market data records`, 'success');
                // Re-analyze with fresh data
                await this.analyzeMarket();
            }
        } catch (error) {
            console.error('Error refreshing market data:', error);
            this.showNotification('Failed to refresh market data', 'error');
        }
    }
    
    async exportAnalysisData() {
        if (!this.currentIndustry || !this.currentProductCategory) {
            this.showNotification('Please perform analysis first', 'warning');
            return;
        }
        
        try {
            const response = await fetch(`/api/v1/global-analytics/market-summary?industry=${this.currentIndustry}&product_category=${this.currentProductCategory}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                // Create CSV export
                const csvContent = this.createCSVExport(data.data);
                this.downloadCSV(csvContent, `global_analytics_${this.currentIndustry}_${this.currentProductCategory}.csv`);
                this.showNotification('Analysis data exported successfully', 'success');
            }
        } catch (error) {
            console.error('Error exporting data:', error);
            this.showNotification('Failed to export data', 'error');
        }
    }
    
    createCSVExport(data) {
        const headers = ['Metric', 'Value', 'Description'];
        const rows = [
            ['Market Penetration', `${data.market_penetration}%`, 'Global market coverage'],
            ['Opportunity Score', `${data.opportunity_score}%`, 'Market opportunity assessment'],
            ['Total Suppliers', data.total_suppliers, 'Number of suppliers analyzed'],
            ['Continents Covered', `${data.continents_covered}/7`, 'Geographic coverage'],
            ['Average Price', `$${data.average_price_usd}`, 'Average product price'],
            ['Compliance Rate', `${data.compliance_rate.toFixed(1)}%`, 'Regulatory compliance']
        ];
        
        const csv = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
        return csv;
    }
    
    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
    
    getColorForMetric(metric) {
        const colors = {
            'supplier_count': 'rgba(54, 162, 235, 0.8)',
            'avg_price': 'rgba(255, 99, 132, 0.8)',
            'avg_quality': 'rgba(75, 192, 192, 0.8)',
            'avg_reliability': 'rgba(255, 205, 86, 0.8)'
        };
        return colors[metric] || 'rgba(153, 102, 255, 0.8)';
    }
    
    showAnalysisProgress() {
        const progressContainer = document.getElementById('analysisProgress');
        if (progressContainer) {
            progressContainer.style.display = 'block';
            progressContainer.innerHTML = `
                <div class="progress-overlay">
                    <div class="progress-content">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <h5 class="mt-3">Analyzing Global Market...</h5>
                        <p>Collecting data from 7 continents and analyzing market intelligence</p>
                    </div>
                </div>
            `;
        }
    }
    
    hideAnalysisProgress() {
        const progressContainer = document.getElementById('analysisProgress');
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
    
    showNotification(message, type = 'info') {
        const notificationContainer = document.getElementById('notificationContainer');
        if (!notificationContainer) return;
        
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[type] || 'alert-info';
        
        const notification = document.createElement('div');
        notification.className = `alert ${alertClass} alert-dismissible fade show`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        notificationContainer.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialize Global Analytics when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.globalAnalytics = new SEEKERGlobalAnalytics();
}); 