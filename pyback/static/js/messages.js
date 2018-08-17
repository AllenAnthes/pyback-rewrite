$(document).ready(() => {
    const $table = $('#message-table').DataTable({order: [[0, 'desc']], iDisplayLength: 100});
    $(document).on('click', '.delete-btn', deleteMessage);

    async function deleteMessage(e) {
        const url = $(e.currentTarget).data('delete');
        const result = await fetch(url);
        const json = await result.json();

        if (json.ok) {
            const $row = $(this).parents('tr');
            $row.fadeOut(400, deleteRow)
        }
    }

    function deleteRow($row) {
        $table.row($row)
            .remove()
            .draw()
    }
});

