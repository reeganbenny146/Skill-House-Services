$(categoryEditModal).on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var name = button.data('name') 
    var id = button.data('id')
    var modal = $(this)
    modal.find('.modal-body #categoryName').val(name)
    modal.find('.modal-body #categoryId').val(id)
  })