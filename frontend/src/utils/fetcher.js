export const fetcher = async (url, { method = "GET", token, headers = {}, body } = {}) => {
    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })
  
    if (!res.ok) {
      const errorBody = await res.text()
      throw new Error(`Fetch failed: ${res.status} ${errorBody}`)
    }
  
    return res.json()
  }
  