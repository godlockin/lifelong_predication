# Fix Frontend Issues and Optimize Data Loading

The issues you reported (Date picker missing, Search invalid) are likely caused by the **huge size of the city data** (~2.5MB) which I embedded directly into the application code in the last update. This caused the deployment to be too large and likely crashed the script execution or hit resource limits.

I will fix this by moving the city data to a **static resource** (`cities.json`) instead of bundling it in the code.

## Plan

1.  **Data Migration & Optimization**
    *   Re-download the city data source.
    *   Generate a `public/cities.json` file containing both the hierarchy (for the cascade menu) and a simplified flat list (for search).
    *   This file will be served as a static asset, keeping the application code small and fast.

2.  **Backend Cleanup**
    *   Remove the massive city data from `src/index.js` and `src/data/cities.js`.
    *   This ensures the Cloudflare Worker stays within size limits and runs reliably.

3.  **Frontend Repair (`public/index.html`)**
    *   **Fix Date Picker:** Ensure `flatpickr` initializes correctly by adding error handling and checking the loading order.
    *   **Fix City Search:** Update the search logic to load from the new `cities.json` file.
    *   **Improve UX:** Ensure the "Search" and "Cascade Select" work together smoothly (e.g., selecting a search result clearly updates the form).

4.  **Verification**
    *   Deploy the changes.
    *   Verify the Date Picker appears and works.
    *   Verify the City Search works and the Cascade menu loads correctly.
