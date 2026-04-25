from fastapi.responses import HTMLResponse

def get_custom_swagger_html(openapi_url: str, title: str) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" >
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"> </script>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"> </script>
        <script>
          window.onload = function() {{
            const ui = SwaggerUIBundle({{
              url: "{openapi_url}",
              dom_id: '#swagger-ui',
              presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
              layout: "StandaloneLayout",
              persistAuthorization: true,

              // This is the key part
              responseInterceptor: (response) => {{
                if (response.url.includes('/auth/login') && response.status === 200) {{
                  const token = response.body?.access_token;
                  if (token) {{
                    ui.preauthorizeApiKey('HTTPBearer', token);
                    console.log('Auth token auto-set from login response');
                  }}
                }}
                return response;
              }}
            }})
            window.ui = ui
          }}
        </script>
      </body>
    </html>
    """
    return HTMLResponse(html)