$(document).ready(() => {
    const $table = $('#logs').DataTable({
        order: [[0, 'desc']],
        pageLength: 100,
        lengthMenu: [[50, 100, 250, 500], [50, 100, 250, 500]],
        ajax: '/api/logs',
        responsive: true,
        columns: [
            {title: 'Timestamp', data: 'timestamp', responsivePriority: 1},
            {title: 'Level', data: 'level', responsivePriority: 2},
            {title: 'Message', data: 'message', responsivePriority: 0}
        ],
        initComplete: () => {
            const filter = $(`
            <div id="filter-wrapper" class="input-field">
                <select multiple id="level-select" title="Filter level">
                    <option value="debug">Debug</option>
                    <option value="info">Info</option>
                    <option value="warning">Warning</option>
                    <option value="error">Error</option>
                </select>
                <label>Filter Level</label>
            </div>
            `);

            $('#logs_wrapper > div:first-of-type > div:first-of-type').append(filter);
            const $select = $('#level-select');
            $select.formSelect();
            $select.on('change', (e) => {
                const levels = $(e.currentTarget).val();
                const term = levels.join('|');
                $table.column(1).search(term, true).draw();
            });
        }
    });
});
