// Fixed disease display function
function displayDiseaseResult(diseaseData) {
    const resultContainer = document.getElementById('disease-result');
    if (!resultContainer) return;
    
    // Initialize variables
    let diseaseInfo, riskLevel, pesticides, preventionTips, forecast;
    
    // Handle both old and new data structures
    if (diseaseData.diseases && diseaseData.diseases.length > 0) {
        // New comprehensive structure
        const primaryDisease = diseaseData.diseases[0];
        diseaseInfo = primaryDisease.disease;
        riskLevel = primaryDisease.risk_level;
        pesticides = primaryDisease.prevention.pesticides || ['Consult agricultural expert'];
        preventionTips = primaryDisease.prevention.management || primaryDisease.prevention.critical_stage || ['Monitor regularly'];
        forecast = diseaseData.forecast_7days;
    } else {
        // Old simple structure
        diseaseInfo = diseaseData.disease || 'Unknown';
        riskLevel = diseaseData.risk_level || 'Low';
        pesticides = diseaseData.pesticides || ['Consult agricultural expert'];
        preventionTips = diseaseData.prevention || ['Monitor regularly'];
        forecast = null;
    }
    
    const riskColor = {
        'High': '#dc3545',
        'Medium': '#ffc107',
        'Low': '#28a745',
        'Unknown': '#6c757d'
    };
    
    const diseaseIcon = diseaseInfo === 'healthy' ? '✓' : '⚠';
    const riskBadgeColor = riskColor[riskLevel] || '#6c757d';
    
    // Build 7-day forecast HTML
    let forecastHtml = '';
    if (forecast && forecast.forecast_available) {
        forecastHtml = `
            <div style="border: 2px solid #007bff; padding: 15px; margin: 20px 0; border-radius: 8px; background: #f8f9fa;">
                <h3 style="text-align: center; color: #007bff; margin-bottom: 15px;">📅 7-Day Disease Risk Forecast</h3>
                <p style="text-align: center; font-style: italic; margin-bottom: 20px;">After 7 days, based on weather predictions, your crop might be affected as follows:</p>
                <div style="background: #e3f2fd; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <h4>📊 Risk Summary:</h4>
                    <ul>
                        <li style="color: #dc3545;">🔴 High Risk Days: ${forecast.summary.high_risk_days}</li>
                        <li style="color: #ffc107;">🟡 Medium Risk Days: ${forecast.summary.medium_risk_days}</li>
                        <li style="color: #28a745;">🟢 Low Risk Days: ${forecast.summary.low_risk_days}</li>
                    </ul>
                </div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; margin: 15px 0;">
                    ${forecast.forecast_days.map(day => `
                        <div style="
                            background: ${day.risk_level === 'High' ? '#ffebeb' : day.risk_level === 'Medium' ? '#fff8e1' : '#e8f5e8'};
                            border: 2px solid ${day.risk_level === 'High' ? '#dc3545' : day.risk_level === 'Medium' ? '#ffc107' : '#28a745'};
                            padding: 10px;
                            border-radius: 5px;
                            text-align: center;
                            font-size: 12px;
                        ">
                            <strong>Day ${day.day}</strong><br>
                            🌡️ ${day.temperature}°C<br>
                            💧 ${day.humidity}%<br>
                            ⚠️ ${day.risk_level}
                        </div>
                    `).join('')}
                </div>
                <div style="background: #e8f5e8; padding: 10px; border-radius: 5px;">
                    <h5>💡 Action Recommendations:</h5>
                    <ul>
                        ${forecast.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }
    
    // Main result HTML
    resultContainer.innerHTML = `
        <div class="disease-prediction-card">
            <div class="disease-header">
                <h3>${diseaseIcon} Disease Prediction Results</h3>
                <div class="risk-badge" style="background-color: ${riskBadgeColor}">
                    Risk Level: ${riskLevel}
                </div>
            </div>
            
            <div class="disease-content">
                <div class="disease-info">
                    <h4>🦠 Predicted Condition</h4>
                    <p class="disease-name">${diseaseInfo.replace('_', ' ').toUpperCase()}</p>
                </div>
                
                <div class="pesticide-recommendations">
                    <h4>🧪 Recommended Pesticides/Fungicides</h4>
                    <div class="pesticide-list">
                        ${pesticides.map(pesticide => `<span class="pesticide-tag" style="background: #e3f2fd; padding: 5px 10px; margin: 3px; border-radius: 15px; display: inline-block;">${pesticide}</span>`).join('')}
                    </div>
                </div>
                
                <div class="prevention-tips">
                    <h4>🛡️ Prevention & Management Tips</h4>
                    <ul class="prevention-list">
                        ${preventionTips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
                
                ${forecastHtml}
                
                <!-- After 7 days Conditions Section -->
                <div style="border: 2px solid #28a745; padding: 15px; margin: 20px 0; border-radius: 8px; background: #f0f8f0;">
                    <h3 style="text-align: center; color: #28a745; margin-bottom: 15px;">🔮 After 7 Days Conditions</h3>
                    <div style="background: #ffffff; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;">
                        <h4 style="color: #28a745;">📈 Expected Disease Progression:</h4>
                        ${diseaseInfo !== 'healthy' ? `
                            <div style="margin: 10px 0;">
                                <p><strong>🔍 Disease Development:</strong> Based on current conditions, <em>${diseaseInfo.replace('_', ' ')}</em> may progress from ${riskLevel.toLowerCase()} to potentially higher risk levels if environmental conditions remain favorable.</p>
                                <p><strong>🌡️ Weather Impact:</strong> Temperature and humidity patterns over the next 7 days will be critical factors in disease development.</p>
                                <p><strong>⚠️ Critical Days:</strong> Days 3-5 are typically most critical for disease establishment and spread.</p>
                            </div>
                            <div style="background: #fff3cd; padding: 10px; border-radius: 5px; border-left: 3px solid #ffc107;">
                                <h5 style="color: #856404;">🎯 What to Expect:</h5>
                                <ul style="margin: 5px 0; padding-left: 20px;">
                                    <li>Symptom visibility may increase if conditions remain favorable</li>
                                    <li>Disease spread rate will depend on humidity and temperature patterns</li>
                                    <li>Early intervention in next 2-3 days can significantly reduce impact</li>
                                    <li>Monitor plants daily for early symptom detection</li>
                                </ul>
                            </div>
                            <div style="background: #d1ecf1; padding: 10px; border-radius: 5px; border-left: 3px solid #17a2b8; margin-top: 10px;">
                                <h5 style="color: #0c5460;">💊 Preventive Action Timeline:</h5>
                                <ul style="margin: 5px 0; padding-left: 20px;">
                                    <li><strong>Day 1-2:</strong> Apply recommended pesticides: ${pesticides.slice(0, 2).join(', ')}</li>
                                    <li><strong>Day 3-4:</strong> Monitor for early symptoms and adjust irrigation</li>
                                    <li><strong>Day 5-7:</strong> Evaluate effectiveness and repeat treatment if necessary</li>
                                </ul>
                            </div>
                        ` : `
                            <div style="margin: 10px 0;">
                                <p><strong>✅ Healthy Outlook:</strong> Current conditions suggest your crop will likely remain healthy over the next 7 days.</p>
                                <p><strong>🌱 Maintenance:</strong> Continue with regular monitoring and preventive care practices.</p>
                                <p><strong>📊 Risk Assessment:</strong> Low probability of disease development based on current environmental conditions.</p>
                            </div>
                            <div style="background: #d4edda; padding: 10px; border-radius: 5px; border-left: 3px solid #28a745;">
                                <h5 style="color: #155724;">🌟 Recommended Actions:</h5>
                                <ul style="margin: 5px 0; padding-left: 20px;">
                                    <li>Maintain current irrigation and fertilization schedule</li>
                                    <li>Continue regular field inspections</li>
                                    <li>Keep preventive treatments ready in case conditions change</li>
                                    <li>Monitor weather forecasts for any sudden changes</li>
                                </ul>
                            </div>
                        `}
                    </div>
                </div>
                
                ${diseaseInfo !== 'healthy' ? `
                    <div class="treatment-advice">
                        <h4>🏥 Treatment Recommendations</h4>
                        <div class="alert alert-warning">
                            <strong>Important:</strong> Consult with local agricultural experts or extension officers for specific treatment plans. This prediction is based on environmental conditions and should be used as a preliminary assessment.
                        </div>
                    </div>
                ` : `
                    <div class="healthy-status">
                        <div class="alert alert-success">
                            <strong>Good News!</strong> Current conditions suggest low disease risk. Continue with regular monitoring and preventive practices.
                        </div>
                    </div>
                `}
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
}
