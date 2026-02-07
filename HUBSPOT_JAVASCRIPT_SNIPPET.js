// HubSpot Landing Page JavaScript
// Copy this entire script and paste it into your HubSpot landing page:
// Settings → Advanced → Custom HTML → Footer HTML
//
// ⚠️ IMPORTANT: Replace YOUR_RAILWAY_URL with your actual Railway URL!

<script>
(function() {
  // ⚠️ REPLACE THIS WITH YOUR RAILWAY URL!
  // Example: https://campaign-automation-production.up.railway.app
  const WEBHOOK_URL = 'YOUR_RAILWAY_URL/webhook/campaign-create';
  
  // Wait for page to load
  window.addEventListener('load', function() {
    // Find HubSpot form
    const form = document.querySelector('form[data-form-id]');
    
    if (!form) {
      console.error('HubSpot form not found');
      return;
    }
    
    console.log('✅ Campaign automation script loaded');
    
    // Listen for form submission
    form.addEventListener('submit', function(e) {
      console.log('📝 Form submitted, preparing webhook call...');
      
      // Let HubSpot process the form first, then call webhook
      setTimeout(function() {
        // Collect form data
        const data = {};
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function(input) {
          const name = input.getAttribute('name') || input.getAttribute('data-name');
          if (name) {
            if (input.type === 'checkbox' || input.type === 'radio') {
              if (input.checked) {
                data[name] = input.value;
              }
            } else {
              data[name] = input.value;
            }
          }
        });
        
        console.log('📦 Collected form data:', data);
        
        // Build payload
        // Map form field names to webhook expected names
        const payload = {
          campaign_name: data.campaign_name || '',
          start_date: data.campaign_start_date || data.start_date || '',
          end_date: data.campaign_end_date || data.end_date || '',
          member_statuses: data.campaign_member_statuses || data.member_statuses || '',
          salesforce_status: data.salesforce_status || 'Planned',
          salesforce_description: data.salesforce_description || '',
          salesforce_type: data.salesforce_type || '',
          parent_campaign: data.parent_campaign || '',
          hubspot_notes: data.hubspot_notes || '',
          wait_minutes: data.wait_minutes || '10',
          webhook_url: data.webhook_url || ''
        };
        
        console.log('🚀 Calling webhook:', WEBHOOK_URL);
        console.log('📤 Payload:', payload);
        
        // Call webhook
        fetch(WEBHOOK_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        })
        .then(response => {
          console.log('📥 Webhook response status:', response.status);
          return response.json();
        })
        .then(result => {
          console.log('✅ Campaign created:', result);
          if (result.status === 'success') {
            alert('🎉 Campaign created successfully!\n\n' +
                  'HubSpot Campaign ID: ' + result.data.hubspot_campaign_id + '\n' +
                  'Salesforce Campaign ID: ' + result.data.salesforce_campaign_id + '\n\n' +
                  'Check HubSpot and Salesforce to verify!');
          } else {
            alert('⚠️ Campaign creation completed with warnings.\n\n' +
                  'Message: ' + result.message + '\n\n' +
                  'Check browser console (F12) for details.');
          }
        })
        .catch(error => {
          console.error('❌ Error creating campaign:', error);
          alert('❌ Error creating campaign.\n\n' +
                'Please check:\n' +
                '1. Railway URL is correct\n' +
                '2. Webhook server is running\n' +
                '3. Browser console (F12) for details\n\n' +
                'Error: ' + error.message);
        });
      }, 1500); // Wait 1.5 seconds for HubSpot to process form
    });
  });
})();
</script>
