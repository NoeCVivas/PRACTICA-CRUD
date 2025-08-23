document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const searchType = document.getElementById('searchType');
    const searchQuery = document.getElementById('searchQuery');
    
    // Obtener las URLs de búsqueda desde el template
    const personaSearchUrl = document.body.getAttribute('data-persona-search-url');
    const oficinaSearchUrl = document.body.getAttribute('data-oficina-search-url');
    
    searchButton.addEventListener('click', function() {
        performSearch();
    });
    
    searchQuery.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    function performSearch() {
        const type = searchType.value;
        const query = searchQuery.value.trim();
        
        if (query === '') {
            return;
        }
        
        let searchUrl;
        if (type === 'persona') {
            searchUrl = personaSearchUrl + "?q=" + encodeURIComponent(query);
        } else if (type === 'oficina') {
            searchUrl = oficinaSearchUrl + "?q=" + encodeURIComponent(query);
        }
        
        window.location.href = searchUrl;
    }
});