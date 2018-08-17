$(document).ready(() => {
    $('#logs').DataTable({
        order: [],
        pageLength: 250,
        lengthMenu: [[50, 100, 250, 500], [50, 100, 250, 500]],
        columns: [{title: 'Log', data: 'log'}],
        ajax: `/api/logs/${level}`
    });
});
