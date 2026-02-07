<script>
(function() {
  // Railway webhook URL
  const WEBHOOK_URL = 'https://campaign-automation-production-c59f.up.railway.app/webhook/campaign-create';
  
  console.log('🔍 Campaign automation script starting...');
  
  // Try multiple ways to find the form
  function findHubSpotForm() {
    // Try different selectors
    const selectors = [
      'form[data-form-id]',
      'form.hs-form',
      'form[id*="form"]',
      'form',
      '.hs-form form',
      '[data-form-id]'
    ];
    
    for (let selector of selectors) {
      const form = document.querySelector(selector);
      if (form) {
        console.log('✅ Found form with selector:', selector);
        return form;
      }
    }
    
    return null;
  }
  
  // Wait for page to load, then try multiple times
  let attempts = 0;
  const maxAttempts = 10;
  
  function tryAttachToForm() {
    attempts++;
    const form = findHubSpotForm();
    
    if (form) {
      console.log('✅ Campaign automation script loaded and form found!');
      
      // Listen for form submission
      form.addEventListener('submit', function(e) {
        console.log('📝 Form submitted, preparing webhook call...');
        
        // Let HubSpot process the form first, then call webhook
        setTimeout(function() {
          // Collect form data
          const data = {};
          const inputs = form.querySelectorAll('input, textarea, select');
          
          console.log('🔍 Found', inputs.length, 'form inputs');
          
          inputs.forEach(function(input) {
            const name = input.getAttribute('name') || input.getAttribute('data-name') || input.getAttribute('id');
            const value = input.value;
            
            if (name && value) {
              console.log('  - Field:', name, '=', value.substring(0, 50));
              if (input.type === 'checkbox' || input.type === 'radio') {
                if (input.checked) {
                  data[name] = value;
                }
              } else {
                data[name] = value;
              }
            }
          });
          
          console.log('📦 Collected form data:', data);
          
          // Build payload - Map form field names to webhook expected names
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
            if (!response.ok) {
              return response.text().then(text => {
                throw new Error(`HTTP ${response.status}: ${text}`);
              });
            }
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
        }, 2000); // Wait 2 seconds for HubSpot to process form
      });
      
      return true; // Successfully attached
    } else if (attempts < maxAttempts) {
      // Form not found yet, try again
      console.log('⏳ Form not found, attempt', attempts, 'of', maxAttempts, '- retrying...');
      setTimeout(tryAttachToForm, 500);
      return false;
    } else {
      console.error('❌ HubSpot form not found after', maxAttempts, 'attempts');
      console.log('💡 Available forms on page:', document.querySelectorAll('form').length);
      return false;
    }
  }
  
  // Start trying when page loads
  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', tryAttachToForm);
  } else {
    tryAttachToForm();
  }
  
  // Also try after a delay in case form loads dynamically
  window.addEventListener('load', function() {
    setTimeout(tryAttachToForm, 1000);
  });
})();
</script>
