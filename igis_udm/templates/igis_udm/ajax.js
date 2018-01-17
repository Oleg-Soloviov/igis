/////////// init scripts ////////////////////////////////
var buttons = document.getElementsByClassName('nomerki')
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', get_ajax_time);
}

var login_button = document.getElementById('login_button');
if (getCookie('family')) {
    login_button.addEventListener('click', ajax_logout);
}
else
{
    login_button.addEventListener('click', show_auth_form);
}

////////////////////////////////////////////////////////////

var dObj; //for debug
var months = ['янв.', 'февр.', 'марта', 'апр.', 'мая', 'июня', 'июля', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.'];
var week_days = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];

////////////////////////////////////////////////////////////
function ajax_login() {
    //Для авторизации
    var xhttp = new XMLHttpRequest();
    var auth_form = document.forms['login'];
    var error_list = document.getElementById('auth-errors-list');
    var overlay = document.getElementById('success_modal_container');
    var overlay_content = document.getElementById('success_modal_content');

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);
        dObj = myObj; //for debug
        if (myObj.status === 'error') {
            var failure_txt = document.createTextNode(myObj['failure']);
            error_list.innerHTML = '';
            error_list.appendChild(failure_txt);
            error_list.style.display = 'block';
            overlay.style.cursor = 'auto';
            overlay.style.display = 'none';
        }
        else if (myObj.status === 'authorized') {
        	patient = JSON.parse(decodeURIComponent(myObj.info));
            var modal = document.getElementById('modal_auth');
            var success_fio_element = document.getElementById('success_fio');
            var patient_fio_element = document.getElementById('patient_fio');
            var patient_fio = patient.f + ' ' + patient.i + ' ' + patient.o;

            patient_fio_element.innerText = patient_fio;
            success_fio_element.innerText = patient_fio;

            var patient_info = document.getElementById('patient_info');
            patient_info.style.display = 'block';
            var therap_uch = document.getElementById('uch_ther');
            therap_uch.innerHTML = 'Терапевтический участок: ' + patient.uch;
            if ( patient.uchg != "0" ){
                var ginecol_uch = document.getElementById('uch_gin');
                ginecol_uch.style.display = 'block';
                ginecol_uch.innerHTML = 'Гинекологический участок: ' + patient.uchg;
            }
            error_list.style.display = 'none';
            error_list.innerHTML = '';
            var login_button = document.getElementById('login_button');
            login_button.innerHTML = 'Выйти';
            login_button.removeEventListener('click', show_auth_form);
            login_button.addEventListener('click', ajax_logout);
            if (myObj.sign_items){
                var zapisi = document.getElementById('zapisi');
                var zapisi_items_div = document.getElementById('zapisi_items');
                zapisi_items_div.innerHTML = '';
                for (var i = 0; i < myObj.sign_items.length; i++) {
                    var panel_div = document.createElement('div');
                    panel_div.className = 'w3-panel w3-border w3-light-grey w3-round-large';

                    var row_div = document.createElement('div');
                    row_div.className = 'w3-row'
                    var el_par = document.createElement('p');
                    var el_text = document.createTextNode(myObj.sign_items[i].sign_specialist_role);
                    el_par.appendChild(el_text);
                    row_div.appendChild(el_par);
                    panel_div.appendChild(row_div);

                    row_div = document.createElement('div');
                    row_div.className = 'w3-row'
                    el_par = document.createElement('p');
                    el_text = document.createTextNode(myObj.sign_items[i].sign_specialist_name);
                    el_par.appendChild(el_text);
                    row_div.appendChild(el_par);
                    panel_div.appendChild(row_div);

                    row_div = document.createElement('div');
                    row_div.className = 'w3-cell-row';

                    var el_div = document.createElement('div');
                    el_div.className = 'w3-cell';
                    el_text = document.createTextNode('Дата и время записи');
                    el_div.appendChild(el_text);
                    row_div.appendChild(el_div);

                    el_div = document.createElement('div');
                    el_div.className = 'w3-cell';
                    el_text = document.createTextNode(myObj.sign_items[i].sign_date)
                    el_div.appendChild(el_text);
                    row_div.appendChild(el_div);

                    el_div = document.createElement('div');
                    el_div.className = 'w3-cell';
                    el_text = document.createTextNode(myObj.sign_items[i].sign_time)
                    el_div.appendChild(el_text);
                    row_div.appendChild(el_div);

                    panel_div.appendChild(row_div);

                    row_div = document.createElement('div');
                    row_div.className = 'w3-row w3-margin-top';
                    var el_button = document.createElement('button');
                    el_text = document.createTextNode('Отменить');
                    el_button.appendChild(el_text);
                    el_button.className = 'w3-button w3-teal w3-margin-bottom w3-round w3-right';
                    //el_button.setAttribute('data-obj', myObj.sign_items[i].obj);
                    el_button.setAttribute('data-id', myObj.sign_items[i].id);
                    el_button.setAttribute('data-date', myObj.sign_items[i].date);
                    el_button.setAttribute('data-time', myObj.sign_items[i].time);
                    el_button.addEventListener('click', sign_out);
//                    el_button.onclick = sign_out;
                    row_div.appendChild(el_button);

                    panel_div.appendChild(row_div);

                    zapisi_items_div.appendChild(panel_div);
                }
                document.getElementById('zapisi_net').style.display = 'none';
                document.getElementById('zapisi_items').style.display = 'block';
            }
            overlay_content.style.display = 'block';
            modal.style.display = 'none';
            overlay.style.cursor = 'auto';

            setCookie('family', patient.f, 1)
            setCookie('name', patient.i, 1)
            setCookie('otchestvo', patient.o, 1)


        }
      }
        //not actual?
      else if (this.readyState == 4 && this.status == 400) {
        var form_errors = JSON.parse(this.responseText);

        if (form_errors.name) {
            for (i in form_errors.name) {
                var li = document.createElement("li");
                var txt = document.createTextNode(form_errors.name[i]);
                li.appendChild(txt);
                name_errors_ul.appendChild(li)};
            name_errors.className = '';
                            };

        if (form_errors.polis) {
            for (i in form_errors.polis) {
                var li = document.createElement("li");
                var txt = document.createTextNode(form_errors.polis[i]);
                li.appendChild(txt);
                polis_errors_ul.appendChild(li)};
            polis_errors.className = ''
                                };
      };
    };

    overlay.style.display = 'block';
    overlay.style.cursor = 'wait';
    xhttp.open("POST", "/udmurtia/login/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", auth_form['csrfmiddlewaretoken'].value);
    var data = 'name=' + auth_form['name'].value + '&polis=' + auth_form['polis'].value;
    xhttp.send(data);

    return false;
}


function ajax_logout() {
    var xhttp = new XMLHttpRequest();
    var auth_form = document.forms['login'];
    var overlay_content = document.getElementById('success_modal_content');
    var success_fio_element = document.getElementById('success_fio');
    success_fio.innerHTML = '';
    var overlay = document.getElementById('success_modal_container');
    overlay_content.style.display = 'none';
    overlay.style.display = 'block';
    overlay.style.cursor = 'wait';


    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);
        dObj = myObj; //for debug
        if (myObj.status === 'error') {
            var failure_txt = document.createTextNode(myObj['failure']);
        }
        else if (myObj.status === 'logout') {
        	var patient_fio_element = document.getElementById('patient_fio');
            patient_fio_element.innerHTML = 'НЕ АВТОРИЗОВАН';
            var login_button = document.getElementById('login_button');
            login_button.innerHTML = 'Авторизация';
            login_button.removeEventListener('click', ajax_logout);
            login_button.addEventListener('click', show_auth_form);

            var patient_info = document.getElementById('patient_info');
            patient_info.style.display = 'none';
            var ginecol_uch = document.getElementById('uch_gin');
            ginecol_uch.style.display = 'none';
            ginecol_uch.innerHTML = '';
            var therap_uch = document.getElementById('uch_ther');
            therap_uch.innerHTML = '';

            var zapisi_items_div = document.getElementById('zapisi_items');
            zapisi_items_div.innerHTML = '';
            document.getElementById('zapisi_net').style.display = 'block';

            document.cookie = "family=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            document.cookie = "otchestvo=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            overlay.style.display = 'none';
            overlay.style.cursor = 'auto';
        }
      }
        //not actual?
      else if (this.readyState == 4 && this.status == 400) {
        var form_errors = JSON.parse(this.responseText);

        if (form_errors.name) {
            for (i in form_errors.name) {
                var li = document.createElement("li");
                var txt = document.createTextNode(form_errors.name[i]);
                li.appendChild(txt);
                name_errors_ul.appendChild(li)};
            name_errors.className = '';
                            };
      };

    };

    xhttp.open("POST", "/udmurtia/logout/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", auth_form['csrfmiddlewaretoken'].value);

    xhttp.send();

    return false;
}


function show_failure(parent_li, myPersonsObj) {
    var button = parent_li.getElementsByClassName('nomerki')
    button[0].removeEventListener('click', get_ajax_time);
    button[0].addEventListener('click', hide_nomerki);
    var date_row_div = document.createElement('div');
    date_row_div.className = 'w3-row w3-margin-top w3-padding w3-border-top';
    var failure_header = document.createElement('h4');
    var failure_text = document.createTextNode(myPersonsObj['failure'])
    failure_header.appendChild(failure_text)
    failure_header.className = 'w3-text-orange'
    date_row_div.appendChild(failure_header)
    parent_li.appendChild(date_row_div)
}


function show_schedule_time(parent_li, myPersonsObj, button) {
    button.removeEventListener('click', get_ajax_time);
    button.addEventListener('click', hide_nomerki);
    for (date_of_sign in myPersonsObj['dates_of_sign']){
        var date_row_div = document.createElement('div');
        date_row_div.className = 'w3-row w3-margin-top w3-padding w3-border-top';
        var date_div = document.createElement('div');
        date_div.className = 'w3-quarter w3-padding-small schedule-date';
        var new_date = new Date(date_of_sign * 1000);
        var date_str = new_date.getDate() + ' ' + months[new_date.getMonth()] + ' (' + week_days[new_date.getDay()] + ')';
        var date_text_node = document.createTextNode(date_str);
        date_div.appendChild(date_text_node);
        date_row_div.appendChild(date_div)

        var time_div = document.createElement('div');
        time_div.className = 'w3-threequarter schedule-time'
        var schedule_time = myPersonsObj['dates_of_sign'][date_of_sign];
        for (var i = 0; i < schedule_time.length; i++){
            var time_button = document.createElement('button');
            if (schedule_time[i][1] == 'false'){
                time_button.className = 'w3-button w3-padding-small w3-green w3-round w3-disabled'
            }else{
                time_button.className = 'w3-button w3-padding-small w3-green w3-round'
            }
            var time_text_node = document.createTextNode(schedule_time[i][0]);
            time_button.setAttribute('data-sign-time', schedule_time[i][0]);
            time_button.setAttribute('data-sign-date', new_date);
            time_button.appendChild(time_text_node);
            time_button.style.margin = '0 2px 2px 0';
            time_button.addEventListener('click', last_alarm_before_signin);
            time_div.appendChild(time_button);
        }
        date_row_div.appendChild(time_div)
        parent_li.appendChild(date_row_div)
    }
}


function sign_person_in() {
    var xhttp = new XMLHttpRequest();
    var auth_form = document.forms['login'];
    var overlay = document.getElementById('signin_modal_container');
    var overlay_content = document.getElementById('signin_modal_content');

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);
        dObj = myObj; // for debug
        if ((myObj.status == 'sign') && myObj.sign_items){
            update_zapisy(myObj.sign_items)
        }
        else {
            alert(myObj.failure)
        }
        overlay.style.display = 'none';
        // очистим last_alarm
        document.getElementById('signin_fio').innerHTML = '';
        document.getElementById('signin_speciality').innerHTML = '';
        document.getElementById('signin_date').innerHTML = '';
        document.getElementById('signin_time').innerHTML = '';

      }
      else if (this.readyState == 4 && this.status != 200) {
        alert(this.statusText)
      }
    }

    overlay_content.style.display = 'none';
    overlay.style.cursor = 'wait';
    xhttp.open("POST", "/udmurtia/signin/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", auth_form['csrfmiddlewaretoken'].value);

    xhttp.send(signin_request_data); // signin_request_data - global variable
}

//выбирает свободные номерки специалиста
function get_ajax_time(evt) {
    var myPersonsObj;
    var xhttp = new XMLHttpRequest();
    var button = this;
    button.disabled = true;
    button.style.cursor = 'wait'
    var parent_li = button.parentElement.parentElement.parentElement.parentElement
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        myPersonsObj = JSON.parse(this.responseText);
        dObj = myPersonsObj;
        if (myPersonsObj['failure']) {
            show_failure(parent_li, myPersonsObj, button)
        } else {
            show_schedule_time(parent_li, myPersonsObj, button)
        }
      } else if (this.readyState == 4) {
        var errors = JSON.parse(this.responseText);
            //document.getElementById('failure_modal_container').style.display='block';
            alert('HTTP status: ' + this.status)
        };
    };
    button.disabled = false;
    button.style.cursor = 'auto'
    var f = document.forms['login'];
    xhttp.open("POST", "{% url 'get_time' %}", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", f['csrfmiddlewaretoken'].value)

    var data = 'id=' + parent_li.getAttribute('data-id');
    xhttp.send(data);
}


function sign_out(el) {
    if (el.type == "click") {
    el = el.target;
    }
    var xhttp = new XMLHttpRequest();
    var auth_form = document.forms['login'];
    var overlay = document.getElementById('signin_modal_container');
    var overlay_content = document.getElementById('signin_modal_content');

    var specialist_id = el.getAttribute('data-id');
    var signout_date = el.getAttribute('data-date');
    var signout_time = el.getAttribute('data-time');
    var signout_obj = el.getAttribute('data-obj');

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);
        dObj = myObj; //for debug
        if (myObj.status == 'signout'){
            update_zapisy(myObj.sign_items.length)
            } else {
                document.getElementById('zapisi_net').style.display = 'block';
                document.getElementById('zapisi_items').style.display = 'none';
                alert(myObj.failure)
            }

        overlay.style.display = 'none';
      }
      else if (this.readyState == 4 && this.status != 200)
      {
        alert(this.statusText)
      }
    }

    overlay_content.style.display = 'none';
    overlay.style.display = 'block';
    overlay.style.cursor = 'wait';
    xhttp.open("POST", "/udmurtia/signout/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", auth_form['csrfmiddlewaretoken'].value);

    var data = 'specialist_id=' + specialist_id + '&date=' + signout_date + '&time=' + signout_time;

    xhttp.send(data);
}