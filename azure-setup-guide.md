# Azure OpenAI Setup Guide

## 🔧 Azure OpenAI Configuration

Your AI Profile Generator has been updated to use Azure OpenAI. Follow these steps to configure it:

### 1. Create Environment File

Create a `.env` file in your project root with these variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_KEY=your_actual_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_VERSION=2024-05-01-preview
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# News API key (optional)
NEWS_API_KEY=your_news_api_key_here
```

### 2. Get Your Azure OpenAI Credentials

From your Azure Portal:

1. **Go to your Azure OpenAI resource**
2. **Get API Key**: 
   - Navigate to "Keys and Endpoint"
   - Copy either KEY 1 or KEY 2
3. **Get Endpoint**: 
   - Same page, copy the "Endpoint" URL
4. **Get Deployment Name**: 
   - Go to "Model deployments" 
   - Copy the name of your deployed model (e.g., "gpt-35-turbo-deployment")

### 3. Install Updated Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test the Configuration

```bash
python ai_processor.py
```

This will run the test function to verify your Azure OpenAI setup.

### 5. Run the Full Application

```bash
python profile_generator.py https://linkedin.com/in/sample-profile --verbose
```

## 🔍 What Changed

- **Import**: Changed from `import openai` to `from openai import AzureOpenAI`
- **Client**: Now uses `AzureOpenAI` client with endpoint and API version
- **API Calls**: Uses deployment name instead of model name
- **Error Handling**: Enhanced for Azure-specific errors
- **Configuration**: New Azure-specific settings in `config.py`

## 🛠 Troubleshooting

### Common Issues:

1. **"Authentication Failed"**
   - Check your API key is correct
   - Verify your endpoint URL format

2. **"Deployment not found"**
   - Verify your deployment name matches exactly
   - Check the deployment is in "Succeeded" state

3. **"Rate limit exceeded"**
   - Your Azure OpenAI quota might be reached
   - Check your Azure OpenAI quota and billing

### Verification Steps:

1. Check your Azure OpenAI resource is deployed
2. Verify your model deployment is active
3. Test API key with a simple curl command:

```bash
curl -X POST "https://your-resource-name.openai.azure.com/openai/deployments/your-deployment-name/chat/completions?api-version=2024-05-01-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: your-api-key" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"max_tokens":10}'
```

## 🚀 Ready to Go!

Once configured, your AI Profile Generator will use Azure OpenAI for enhanced security and enterprise compliance. 