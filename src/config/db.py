from supabase import create_client

url = "https://tpoqoozkwbcejhuyouhl.supabase.co"
api = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3Fvb3prd2JjZWpodXlvdWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ1OTQxNTAsImV4cCI6MjA4MDE3MDE1MH0.z0UtY9Yw8ggn5r-5Sb65vKr66-awvH2biE6l0sWkNuE"

db = create_client(url, api)