msgSendId = 1;
success = false;

function checkSuccess(data) {
	success = (data == "1");
}
function showStatus(mhide, text, flag){
	var modalObj2 = $('#statusModal');
	var statusButton = modalObj2.find('.modal-footer').find('button#statusButton');
	var textField = modalObj2.find('.modal-body').find("p#result");
	statusButton.removeClass('btn-success').removeClass('btn-danger');
	if(flag){
		statusButton.addClass('btn-success');
		textField.text(text);
	}else{
		statusButton.addClass('btn-danger');
		textField.text(text);
	}
	mhide.modal('hide');
	modalObj2.modal('show');
}

$(document).ready(function() {
	$('#tab-overview').find('#content').load(
		'overviewList',
	);
	users_searchUrlExecute();
	companies_searchUrlExecute();
	admins_searchUrlExecute();
	courses_searchUrlExecute();
	news_searchUrlExecute();
	msg_searchUrlExecute();
});


////////////////

function admins_add(th){
	var modalObj = $('#addModal');
	var th2 = $(th);
	
	var form = modalObj.find('.modal-body').find("#editForm");
	form.find("#1").val('');
	form.find("#2").val('');
	form.find("#3").val('');
	form.find("#4").val('');
	
	modalObj.modal('show');
}
function admins_addConfirm(th){
	var modalObj = $('#addModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['login'] = form.find("#1").val();
	query['password'] = form.find("#2").val();
	query['first_name'] = form.find("#3").val();
	query['last_name'] = form.find("#4").val();
	
	$.ajax({
		type: 'GET',
		url: 'adminsAdd',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = 'Administrator ' + form.find("#1").val() + ' został dodany pomyślnie.';
			}else{
				textShow = 'Wystąpił błąd podczas dodawania administratora ' + form.find("#1").val() + '.';
			}
			
			showStatus(modalObj, textShow, success)
			admins_searchUrlExecute();
		}
	});
	
}

function msgNotify(sid){
	var query = {};
	if(sid != null){
		query['id'] = sid;
	}
	$.ajax({
		type: 'GET',
		url: 'msgNotify',
		data: query,
		success: function(data) {
			var msgCnt = data;
			var cont = $('a#msgCounterContainer');
			cont.empty();
			if(msgCnt > 0){
				cont.append("Wiadomości <span id=\"msgCounter\" style=\"margin-left: 5px;\" class=\"badge badge-primary\">" + msgCnt + "</span>");
			}else{
				cont.append("Wiadomości");
			}
		}
	});
}

function msg_showMessageModal(th, id){
	var modalObj = $('#msgModal');
	var th2 = $(th);
	msg_attrObj = th2.parent().parent();
	
	msgSendId = id;
	
	var unread = msg_attrObj.hasClass('bg-warning');
	if ( unread ){
		msg_attrObj.removeClass('bg-warning');
		/*
		var msgCnt = $('span#msgCounter').text();
		msgCnt -= 1;
		if(msgCnt <= 0){
			$('span#msgCounter').remove();
		}else{
			$('span#msgCounter').text(msgCnt);
		}*/
		msgNotify(id);
	}
	
	msgNotify(id);
	
	
	
	var query = {};
	query['id'] = id;
	
	modalObj.find('.modal-title').text("Wiadomość od " + msg_attrObj.find('#1').text());
	var editForm = modalObj.find('.modal-body').find("#editForm");
	editForm.load(
		'msgSendForm',
		$.param(query)
	);
	
	modalObj.modal('show');
}
function msg_confirmSendModal(th){
	var modalObj = $('#msgModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['id'] = msgSendId;
	query['subject'] = form.find("#1").val();
	query['content'] = form.find("#2").val();
	
	$.ajax({
		type: 'GET',
		url: 'msgSend',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = 'Wiadomość została wysłana.';
			}else{
				textShow = 'Wystąpił błąd podczas wysyłania wiadomości';
			}
			
			showStatus(modalObj, textShow, success)
			msg_searchUrlExecute();
		}
	});
	
}

///////////////////////////


users_currentSearchPhrase = '';
users_currentPage = 1;
users_currentCount = 1;
users_currentCategory = 1;

users_currentSortColumn = 1;

users_currentSortOrder = 1;

users_attrObj = null;






function users_showEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	users_attrObj = th2.parent().parent();
	//users_attrObj = $('tbody#users_tbody').find('tr#' + n);
	
	var query = {};
	query['id'] = users_attrObj.find('#1').text();
	
	modalObj.find('.modal-title').text('Edycja danych kursanta');
	var editForm = modalObj.find('.modal-body').find("#editForm");
	editForm.load(
		'usersEditForm',
		$.param(query)
	);
	
	
	var confirmButton = modalObj.find('.modal-footer').find('#editButton');
	confirmButton.unbind('click');
	confirmButton.on('click', users_confirmEditModal);
	modalObj.modal('show');
}





function users_confirmEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['id'] = users_attrObj.find('#1').text();
	
	query['password'] = form.find("#1").val();
	
	query['name'] = form.find("#2").val();
	
	query['surname'] = form.find("#3").val();
	
	query['city'] = form.find("#4").val();
	
	query['street'] = form.find("#5").val();
	
	query['house_number'] = form.find("#6").val();
	
	query['flat_number'] = form.find("#7").val();
	
	
	$.ajax({
		type: 'GET',
		url: 'usersUpdate',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Dane użytkownika '" + users_attrObj.find('#2').text() + "' zostały zaktualizowane.";
			}else{
				textShow = "Wystąpił błąd podczas aktualizacji danych użytkownika '" + users_attrObj.find('#2').text() + "'.";
			}
			
			showStatus(modalObj, textShow, success)
			users_searchUrlExecute();
		}
	});
	
}



function users_confirmRemoveModal(th){
	var modalObj1 = $('#deleteModal');
	var th2 = $(th);
	
	var query = {};
	query['id'] = users_attrObj.find('#1').text();
	
	$.ajax({
		type: 'GET',
		url: 'usersDelete',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Użytkownik '" + users_attrObj.find('#2').text() + "' został usunięty.";
			}else{
				textShow = "Wystąpił błąd podczas usuwania użytkownika '" + users_attrObj.find('#2').text() + "'.";
			}
			showStatus(modalObj1, textShow, success);
			users_searchUrlExecute();
		}
	});
}
function users_sort(th, col){
	var $sortable = $('#tab-users').find('.sortable');
	var $this = $(th);
	var asc = $this.hasClass('asc');
	var desc = $this.hasClass('desc');
	$sortable.removeClass('asc').removeClass('desc');
	if (desc || (!asc && !desc)) {
		$this.addClass('asc');
		users_currentSortOrder = 1;
	} else {
		$this.addClass('desc');
		users_currentSortOrder = 0;
	}
	users_currentSortColumn = col;
	users_searchUrlExecute();
}
function users_showRemoveModal(th){
	var modalObj = $('#deleteModal');
	var th2 = $(th);
	users_attrObj = th2.parent().parent();
	modalObj.find('.modal-title').text('Usuwanie użytkownika');
	modalObj.find('.modal-body').find("p#deleteDesc").text("Czy na pewno chcesz usunąć użytkownika: " + users_attrObj.find('#2').text());
	var confirmButton = modalObj.find('.modal-footer').find('#deleteButton');
	confirmButton.unbind('click');
	confirmButton.on('click', users_confirmRemoveModal);
	modalObj.modal('show');
}
function users_onSearchClick(){
	var tab = $('#tab-users');
	users_currentPage = 1;
	users_currentSearchPhrase = tab.find("#searchInput").val();
	users_currentCount = tab.find("#countSelect").val();
	users_currentCategory = tab.find("#categorySelect").val();
	users_searchUrlExecute();
}
function users_onPage(num){
	users_currentPage = num;
	users_searchUrlExecute();
}
function users_searchUrlExecute(){
	var query = {};
	query['search'] = users_currentSearchPhrase;
	query['page'] = users_currentPage;
	query['display'] = users_currentCount;
	query['filter'] = users_currentCategory;
	query['sortcol'] = users_currentSortColumn;
	query['sortord'] = users_currentSortOrder;
	
	$('#tab-users').find('#content').load(
		'usersList',
		$.param(query)
	);
	
	
}
companies_currentSearchPhrase = '';
companies_currentPage = 1;
companies_currentCount = 1;
companies_currentCategory = 1;

companies_currentSortColumn = 1;

companies_currentSortOrder = 1;

companies_attrObj = null;






function companies_showEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	companies_attrObj = th2.parent().parent();
	//companies_attrObj = $('tbody#companies_tbody').find('tr#' + n);
	
	var query = {};
	query['id'] = companies_attrObj.find('#1').text();
	
	modalObj.find('.modal-title').text('Edycja danych firmy szkoleniowej');
	var editForm = modalObj.find('.modal-body').find("#editForm");
	editForm.load(
		'companiesEditForm',
		$.param(query)
	);
	
	
	var confirmButton = modalObj.find('.modal-footer').find('#editButton');
	confirmButton.unbind('click');
	confirmButton.on('click', companies_confirmEditModal);
	modalObj.modal('show');
}





function companies_confirmEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['id'] = companies_attrObj.find('#1').text();
	
	query['password'] = form.find("#1").val();
	
	query['company_name'] = form.find("#2").val();
	
	query['city'] = form.find("#3").val();
	
	query['street'] = form.find("#4").val();
	
	query['house_number'] = form.find("#5").val();
	
	query['flat_number'] = form.find("#6").val();
	
	
	$.ajax({
		type: 'GET',
		url: 'companiesUpdate',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Dane firmy szkoleniowej '" + companies_attrObj.find('#2').text() + "' zostały zaktualizowane.";
			}else{
				textShow = "Wystąpił błąd podczas aktualizacji danych firmy szkoleniowej '" + companies_attrObj.find('#2').text() + "'.";
			}
			
			showStatus(modalObj, textShow, success)
			companies_searchUrlExecute();
		}
	});
	
}



function companies_confirmRemoveModal(th){
	var modalObj1 = $('#deleteModal');
	var th2 = $(th);
	
	var query = {};
	query['id'] = companies_attrObj.find('#1').text();
	
	$.ajax({
		type: 'GET',
		url: 'companiesDelete',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Firma szkoleniowa '" + companies_attrObj.find('#2').text() + "' została usunięta.";
			}else{
				textShow = "Wystąpił błąd podczas usuwania firmy szkoleniowej '" + companies_attrObj.find('#2').text() + "'.";
			}
			showStatus(modalObj1, textShow, success);
			companies_searchUrlExecute();
		}
	});
}
function companies_sort(th, col){
	var $sortable = $('#tab-companies').find('.sortable');
	var $this = $(th);
	var asc = $this.hasClass('asc');
	var desc = $this.hasClass('desc');
	$sortable.removeClass('asc').removeClass('desc');
	if (desc || (!asc && !desc)) {
		$this.addClass('asc');
		companies_currentSortOrder = 1;
	} else {
		$this.addClass('desc');
		companies_currentSortOrder = 0;
	}
	companies_currentSortColumn = col;
	companies_searchUrlExecute();
}
function companies_showRemoveModal(th){
	var modalObj = $('#deleteModal');
	var th2 = $(th);
	companies_attrObj = th2.parent().parent();
	modalObj.find('.modal-title').text('Usuwanie firmy szkoleniowej');
	modalObj.find('.modal-body').find("p#deleteDesc").text("Czy na pewno chcesz usunąć firmę szkoleniową: " + companies_attrObj.find('#2').text());
	var confirmButton = modalObj.find('.modal-footer').find('#deleteButton');
	confirmButton.unbind('click');
	confirmButton.on('click', companies_confirmRemoveModal);
	modalObj.modal('show');
}
function companies_onSearchClick(){
	var tab = $('#tab-companies');
	companies_currentPage = 1;
	companies_currentSearchPhrase = tab.find("#searchInput").val();
	companies_currentCount = tab.find("#countSelect").val();
	companies_currentCategory = tab.find("#categorySelect").val();
	companies_searchUrlExecute();
}
function companies_onPage(num){
	companies_currentPage = num;
	companies_searchUrlExecute();
}
function companies_searchUrlExecute(){
	var query = {};
	query['search'] = companies_currentSearchPhrase;
	query['page'] = companies_currentPage;
	query['display'] = companies_currentCount;
	query['filter'] = companies_currentCategory;
	query['sortcol'] = companies_currentSortColumn;
	query['sortord'] = companies_currentSortOrder;
	
	$('#tab-companies').find('#content').load(
		'companiesList',
		$.param(query)
	);
	
	
}
admins_currentSearchPhrase = '';
admins_currentPage = 1;
admins_currentCount = 1;
admins_currentCategory = 1;

admins_currentSortColumn = 1;

admins_currentSortOrder = 1;

admins_attrObj = null;






function admins_showEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	admins_attrObj = th2.parent().parent();
	//admins_attrObj = $('tbody#admins_tbody').find('tr#' + n);
	
	var query = {};
	query['id'] = admins_attrObj.find('#1').text();
	
	modalObj.find('.modal-title').text('Edycja danych administratora');
	var editForm = modalObj.find('.modal-body').find("#editForm");
	editForm.load(
		'adminsEditForm',
		$.param(query)
	);
	
	
	var confirmButton = modalObj.find('.modal-footer').find('#editButton');
	confirmButton.unbind('click');
	confirmButton.on('click', admins_confirmEditModal);
	modalObj.modal('show');
}





function admins_confirmEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['id'] = admins_attrObj.find('#1').text();
	
	query['password'] = form.find("#1").val();
	
	query['first_name'] = form.find("#2").val();
	
	query['last_name'] = form.find("#3").val();
	
	
	$.ajax({
		type: 'GET',
		url: 'adminsUpdate',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Dane administratora '" + admins_attrObj.find('#2').text() + "' zostały zaktualizowane.";
			}else{
				textShow = "Wystąpił błąd podczas aktualizacji danych administratora '" + admins_attrObj.find('#2').text() + "'.";
			}
			
			showStatus(modalObj, textShow, success)
			admins_searchUrlExecute();
		}
	});
	
}



function admins_confirmRemoveModal(th){
	var modalObj1 = $('#deleteModal');
	var th2 = $(th);
	
	var query = {};
	query['id'] = admins_attrObj.find('#1').text();
	
	$.ajax({
		type: 'GET',
		url: 'adminsDelete',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Administrator '" + admins_attrObj.find('#2').text() + "' został usunięty.";
			}else{
				textShow = "Wystąpił błąd podczas usuwania administratora '" + admins_attrObj.find('#2').text() + "'.";
			}
			showStatus(modalObj1, textShow, success);
			admins_searchUrlExecute();
		}
	});
}
function admins_sort(th, col){
	var $sortable = $('#tab-admins').find('.sortable');
	var $this = $(th);
	var asc = $this.hasClass('asc');
	var desc = $this.hasClass('desc');
	$sortable.removeClass('asc').removeClass('desc');
	if (desc || (!asc && !desc)) {
		$this.addClass('asc');
		admins_currentSortOrder = 1;
	} else {
		$this.addClass('desc');
		admins_currentSortOrder = 0;
	}
	admins_currentSortColumn = col;
	admins_searchUrlExecute();
}
function admins_showRemoveModal(th){
	var modalObj = $('#deleteModal');
	var th2 = $(th);
	admins_attrObj = th2.parent().parent();
	modalObj.find('.modal-title').text('Usuwanie administratora');
	modalObj.find('.modal-body').find("p#deleteDesc").text("Czy na pewno chcesz usunąć administratora: " + admins_attrObj.find('#2').text());
	var confirmButton = modalObj.find('.modal-footer').find('#deleteButton');
	confirmButton.unbind('click');
	confirmButton.on('click', admins_confirmRemoveModal);
	modalObj.modal('show');
}
function admins_onSearchClick(){
	var tab = $('#tab-admins');
	admins_currentPage = 1;
	admins_currentSearchPhrase = tab.find("#searchInput").val();
	admins_currentCount = tab.find("#countSelect").val();
	admins_currentCategory = tab.find("#categorySelect").val();
	admins_searchUrlExecute();
}
function admins_onPage(num){
	admins_currentPage = num;
	admins_searchUrlExecute();
}
function admins_searchUrlExecute(){
	var query = {};
	query['search'] = admins_currentSearchPhrase;
	query['page'] = admins_currentPage;
	query['display'] = admins_currentCount;
	query['filter'] = admins_currentCategory;
	query['sortcol'] = admins_currentSortColumn;
	query['sortord'] = admins_currentSortOrder;
	
	$('#tab-admins').find('#content').load(
		'adminsList',
		$.param(query)
	);
	
	
}
courses_currentSearchPhrase = '';
courses_currentPage = 1;
courses_currentCount = 1;
courses_currentCategory = 1;

courses_currentSortColumn = 1;

courses_currentSortOrder = 1;

courses_attrObj = null;



function courses_lookup(th){
	var th2 = $(th);
	courses_attrObj = th2.parent().parent();
	
	var id = courses_attrObj.find('#1').text();
	
	var url = '../course_details' + '/' + id + '/'
	
	var win = window.open(url, '_blank');
	win.focus();
}




function courses_showEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	courses_attrObj = th2.parent().parent();
	//courses_attrObj = $('tbody#courses_tbody').find('tr#' + n);
	
	var query = {};
	query['id'] = courses_attrObj.find('#1').text();
	
	modalObj.find('.modal-title').text('Edycja danych kursu');
	var editForm = modalObj.find('.modal-body').find("#editForm");
	editForm.load(
		'coursesEditForm',
		$.param(query)
	);
	
	
	var confirmButton = modalObj.find('.modal-footer').find('#editButton');
	confirmButton.unbind('click');
	confirmButton.on('click', courses_confirmEditModal);
	modalObj.modal('show');
}





function courses_confirmEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['id'] = courses_attrObj.find('#1').text();
	
	query['title'] = form.find("#1").val();
	
	query['start_date'] = form.find("#2").val();
	
	query['price'] = form.find("#4").val();
	
	query['region'] = form.find("#5").val();
	
	query['city'] = form.find("#6").val();
	
	query['category'] = form.find("#7").val();
	
	query['subcategory'] = form.find("#8").val();
	
	query['max_students'] = form.find("#9").val();
	
	query['has_certificate'] = form.find("#10").val();
	
	
	$.ajax({
		type: 'GET',
		url: 'coursesUpdate',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Dane kursu '" + courses_attrObj.find('#2').text() + "' zostały zaktualizowane.";
			}else{
				textShow = "Wystąpił błąd podczas aktualizacji danych kursu '" + courses_attrObj.find('#2').text() + "'.";
			}
			
			showStatus(modalObj, textShow, success)
			courses_searchUrlExecute();
		}
	});
	
}



function courses_confirmRemoveModal(th){
	var modalObj1 = $('#deleteModal');
	var th2 = $(th);
	
	var query = {};
	query['id'] = courses_attrObj.find('#1').text();
	
	$.ajax({
		type: 'GET',
		url: 'coursesDelete',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Kurs '" + courses_attrObj.find('#2').text() + "' został usunięty.";
			}else{
				textShow = "Wystąpił błąd podczas usuwania kursu '" + courses_attrObj.find('#2').text() + "'.";
			}
			showStatus(modalObj1, textShow, success);
			courses_searchUrlExecute();
		}
	});
}
function courses_sort(th, col){
	var $sortable = $('#tab-courses').find('.sortable');
	var $this = $(th);
	var asc = $this.hasClass('asc');
	var desc = $this.hasClass('desc');
	$sortable.removeClass('asc').removeClass('desc');
	if (desc || (!asc && !desc)) {
		$this.addClass('asc');
		courses_currentSortOrder = 1;
	} else {
		$this.addClass('desc');
		courses_currentSortOrder = 0;
	}
	courses_currentSortColumn = col;
	courses_searchUrlExecute();
}
function courses_showRemoveModal(th){
	var modalObj = $('#deleteModal');
	var th2 = $(th);
	courses_attrObj = th2.parent().parent();
	modalObj.find('.modal-title').text('Usuwanie kursu');
	modalObj.find('.modal-body').find("p#deleteDesc").text("Czy na pewno chcesz usunąć kurs: " + courses_attrObj.find('#2').text());
	var confirmButton = modalObj.find('.modal-footer').find('#deleteButton');
	confirmButton.unbind('click');
	confirmButton.on('click', courses_confirmRemoveModal);
	modalObj.modal('show');
}
function courses_onSearchClick(){
	var tab = $('#tab-courses');
	courses_currentPage = 1;
	courses_currentSearchPhrase = tab.find("#searchInput").val();
	courses_currentCount = tab.find("#countSelect").val();
	courses_currentCategory = tab.find("#categorySelect").val();
	courses_searchUrlExecute();
}
function courses_onPage(num){
	courses_currentPage = num;
	courses_searchUrlExecute();
}
function courses_searchUrlExecute(){
	var query = {};
	query['search'] = courses_currentSearchPhrase;
	query['page'] = courses_currentPage;
	query['display'] = courses_currentCount;
	query['filter'] = courses_currentCategory;
	query['sortcol'] = courses_currentSortColumn;
	query['sortord'] = courses_currentSortOrder;
	
	$('#tab-courses').find('#content').load(
		'coursesList',
		$.param(query)
	);
	
	
}
news_currentSearchPhrase = '';
news_currentPage = 1;
news_currentCount = 1;
news_currentCategory = 1;

news_currentSortColumn = 1;

news_currentSortOrder = 1;

news_attrObj = null;



function news_lookup(th){
	var th2 = $(th);
	news_attrObj = th2.parent().parent();
	
	var id = news_attrObj.find('#1').text();
	
	var url = '../post' + '/' + id + '/'
	
	var win = window.open(url, '_blank');
	win.focus();
}



function news_showEditModal(th){
	var th2 = $(th);
	news_attrObj = th2.parent().parent();
	
	var id = news_attrObj.find('#1').text();
	
	var url = '../post' + '/' + id + '/update'
	
	var win = window.open(url, '_blank');
	win.focus();
}




function news_confirmEditModal(th){
	var modalObj = $('#editModal');
	var th2 = $(th);
	var form = modalObj.find('.modal-body').find("#editForm");
	
	var query = {};
	query['id'] = news_attrObj.find('#1').text();
	
	query['title'] = form.find("#1").val();
	
	query['timestamp'] = form.find("#2").val();
	
	query['view_count'] = form.find("#3").val();
	
	query['comment_count'] = form.find("#4").val();
	
	query['featured'] = form.find("#5").val();
	
	
	$.ajax({
		type: 'GET',
		url: 'newsUpdate',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Dane news\'a '" + news_attrObj.find('#2').text() + "' zostały zaktualizowane.";
			}else{
				textShow = "Wystąpił błąd podczas aktualizacji danych news\'a '" + news_attrObj.find('#2').text() + "'.";
			}
			
			showStatus(modalObj, textShow, success)
			news_searchUrlExecute();
		}
	});
	
}



function news_confirmRemoveModal(th){
	var modalObj1 = $('#deleteModal');
	var th2 = $(th);
	
	var query = {};
	query['id'] = news_attrObj.find('#1').text();
	
	$.ajax({
		type: 'GET',
		url: 'newsDelete',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "News '" + news_attrObj.find('#2').text() + "' został usunięty.";
			}else{
				textShow = "Wystąpił błąd podczas usuwania news\'a '" + news_attrObj.find('#2').text() + "'.";
			}
			showStatus(modalObj1, textShow, success);
			news_searchUrlExecute();
		}
	});
}
function news_sort(th, col){
	var $sortable = $('#tab-news').find('.sortable');
	var $this = $(th);
	var asc = $this.hasClass('asc');
	var desc = $this.hasClass('desc');
	$sortable.removeClass('asc').removeClass('desc');
	if (desc || (!asc && !desc)) {
		$this.addClass('asc');
		news_currentSortOrder = 1;
	} else {
		$this.addClass('desc');
		news_currentSortOrder = 0;
	}
	news_currentSortColumn = col;
	news_searchUrlExecute();
}
function news_showRemoveModal(th){
	var modalObj = $('#deleteModal');
	var th2 = $(th);
	news_attrObj = th2.parent().parent();
	modalObj.find('.modal-title').text('Usuwanie news\'a');
	modalObj.find('.modal-body').find("p#deleteDesc").text("Czy na pewno chcesz usunąć news: " + news_attrObj.find('#2').text());
	var confirmButton = modalObj.find('.modal-footer').find('#deleteButton');
	confirmButton.unbind('click');
	confirmButton.on('click', news_confirmRemoveModal);
	modalObj.modal('show');
}
function news_onSearchClick(){
	var tab = $('#tab-news');
	news_currentPage = 1;
	news_currentSearchPhrase = tab.find("#searchInput").val();
	news_currentCount = tab.find("#countSelect").val();
	news_currentCategory = tab.find("#categorySelect").val();
	news_searchUrlExecute();
}
function news_onPage(num){
	news_currentPage = num;
	news_searchUrlExecute();
}
function news_searchUrlExecute(){
	var query = {};
	query['search'] = news_currentSearchPhrase;
	query['page'] = news_currentPage;
	query['display'] = news_currentCount;
	query['filter'] = news_currentCategory;
	query['sortcol'] = news_currentSortColumn;
	query['sortord'] = news_currentSortOrder;
	
	$('#tab-news').find('#content').load(
		'newsList',
		$.param(query)
	);
	
	
}
msg_currentSearchPhrase = '';
msg_currentPage = 1;
msg_currentCount = 1;
msg_currentCategory = 1;

msg_currentSortColumn = 4;

msg_currentSortOrder = 1;

msg_attrObj = null;












function msg_confirmRemoveModal(th){
	var modalObj1 = $('#deleteModal');
	var th2 = $(th);
	
	var query = {};
	query['id'] = msg_attrObj.find('#1').text();
	
	$.ajax({
		type: 'GET',
		url: 'msgDelete',
		data: query,
		success: function(data) {
			checkSuccess(data);
			if(success){
				textShow = "Wiadomość od '" + msg_attrObj.find('#1').text() + "' została usunięta.";
			}else{
				textShow = "Wystąpił błąd podczas usuwania wiadomości od '" + msg_attrObj.find('#1').text() + "'.";
			}
			showStatus(modalObj1, textShow, success);
			msg_searchUrlExecute();
		}
	});
}
function msg_sort(th, col){
	var $sortable = $('#tab-msg').find('.sortable');
	var $this = $(th);
	var asc = $this.hasClass('asc');
	var desc = $this.hasClass('desc');
	$sortable.removeClass('asc').removeClass('desc');
	if (desc || (!asc && !desc)) {
		$this.addClass('asc');
		msg_currentSortOrder = 1;
	} else {
		$this.addClass('desc');
		msg_currentSortOrder = 0;
	}
	msg_currentSortColumn = col;
	msg_searchUrlExecute();
}
function msg_showRemoveModal(th){
	var modalObj = $('#deleteModal');
	var th2 = $(th);
	msg_attrObj = th2.parent().parent();
	modalObj.find('.modal-title').text('Usuwanie wiadmości');
	modalObj.find('.modal-body').find("p#deleteDesc").text("Czy na pewno chcesz usunąć wiadomość od: " + msg_attrObj.find('#1').text());
	var confirmButton = modalObj.find('.modal-footer').find('#deleteButton');
	confirmButton.unbind('click');
	confirmButton.on('click', msg_confirmRemoveModal);
	modalObj.modal('show');
}
function msg_onSearchClick(){
	var tab = $('#tab-msg');
	msg_currentPage = 1;
	msg_currentSearchPhrase = tab.find("#searchInput").val();
	msg_currentCount = tab.find("#countSelect").val();
	msg_currentCategory = tab.find("#categorySelect").val();
	msg_searchUrlExecute();
}
function msg_onPage(num){
	msg_currentPage = num;
	msg_searchUrlExecute();
}
function msg_searchUrlExecute(){
	var query = {};
	query['search'] = msg_currentSearchPhrase;
	query['page'] = msg_currentPage;
	query['display'] = msg_currentCount;
	query['filter'] = msg_currentCategory;
	query['sortcol'] = msg_currentSortColumn;
	query['sortord'] = msg_currentSortOrder;
	
	$('#tab-msg').find('#content').load(
		'msgList',
		$.param(query)
	);
	
	
	msgNotify(null);
	
}