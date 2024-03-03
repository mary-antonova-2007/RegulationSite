document.addEventListener('DOMContentLoaded', function() {
    function updatePredecessors(projectId) {
        // AJAX-запрос для получения задач
        fetch(`/get-tasks-for-project/${projectId}/`)
            .then(response => response.json())
            .then(data => {
                // Обновление списка predecessors
            });
    }

    // Слушатель событий для поля project и product
    document.getElementById('id_project').addEventListener('change', function() {
        updatePredecessors(this.value);
    });

    document.getElementById('id_product').addEventListener('change', function() {
        // Подумайте о том, как получить projectId из product
        updatePredecessors(projectId);
    });
});
