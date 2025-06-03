def build_email_html(fields: dict, article_html: str) -> str:
    return f"""
    <html>
    <body style="font-family:Segoe UI, sans-serif; color:#333; line-height:1.6; padding:20px;">
        <h2 style="color:#2F5496;">📢 SLT Article Alert</h2>
        <table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
            <tr><td><strong>Campaign ID:</strong></td><td>{fields.get('campaignId','')}</td></tr>
            <tr><td><strong>Campaign Name:</strong></td><td>{fields.get('campaignName','')}</td></tr>
            <tr><td><strong>Published:</strong></td><td>{fields.get('publishingDate','')}</td></tr>
            <tr><td><strong>Title:</strong></td><td>{fields.get('articleTitle','')}</td></tr>
            <tr><td><strong>URL:</strong></td><td><a href="{fields.get('articleURL','')}">{fields.get('articleURL','')}</a></td></tr>
        </table>

        <p><strong>Snippet:</strong></p>
        <blockquote style="background:#f9f9f9; padding:10px; border-left:4px solid #ccc;">
            {fields.get('articleSnippet','')}
        </blockquote>

        <hr style="margin:30px 0;" />

        <h3>📰 Full Article</h3>
        <div style="background:#fff8dc; padding:15px; border:1px solid #e3e3e3;">
            {article_html}
        </div>

        <p style="font-size:12px; color:#888;">This alert was automatically generated based on SLT campaign filters.</p>
    </body>
    </html>
    """