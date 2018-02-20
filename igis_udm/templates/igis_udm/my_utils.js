var full_months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
var full_week_days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];

function hide_nomerki() {
    var parent_li = this.parentElement.parentElement.parentElement;
    var hide_rows = parent_li.getElementsByClassName('w3-border-top');
    hide_rows = Array.prototype.slice.call(hide_rows);
    var rows_length = hide_rows.length
    for (var i = 0; i < rows_length; i++){
        var x = hide_rows.pop();
        parent_li.removeChild(x);
    }
    this.removeEventListener('click', hide_nomerki);
    this.addEventListener('click', get_ajax_time);
    this.innerHTML = 'Номерки';
}

function show_auth_form(){
    var modal = document.getElementById('modal_auth');
    var error_list = document.getElementById('auth-errors-list');
    error_list.style.display = 'none';
    error_list.innerHTML = '';
    modal.style.display = 'block';
}

function closeAuthForm(){
    var modal = document.getElementById('modal_auth');
    var auth_form = document.forms['login'];
    var header = modal.getElementsByTagName('h2')[0];

    auth_form.className = 'w3-margin-bottom';
    header.innerHTML = 'Авторизация';
    header.parentElement.className = 'w3-container w3-teal';
    modal.style.display = 'none';
}

function closeSuccessAuth(){
    var overlay = document.getElementById('success_modal_container');
    overlay.style.display = 'none';
    var overlay_content = document.getElementById('success_modal_content');
    overlay_content.style.display = 'none';
    var success_fio = document.getElementById('success_fio');
    success_fio.innerHTML = '';
}

function closeSignIn(){
    var overlay = document.getElementById('signin_modal_container');
    overlay.style.display = 'none';
    signin_request_data = null;
    document.getElementById('signin_fio').innerHTML = '';
    document.getElementById('signin_speciality').innerHTML = '';
    document.getElementById('signin_date').innerHTML = '';
    document.getElementById('signin_time').innerHTML = '';
}

function toggle_class(id, cls){
    // id - елемент
    //cls - класс
    var a;
    a = document.getElementById(id);
    if (a.classList.contains(cls)) {
        a.classList.remove(cls);
    } else {
        a.classList.add(cls)
    }
}

function filterHTML (id, sel, sel_where, filter) {
    //id - елемент-родитель, перерчисляем через пробел
    //sel - class что будет отфильтрованно
    //sel_where - class где конкретно искать строку для фильтрации
    //filter - строка фильтрации
  var a, b, c, d, i, ii, iii, iiii, hit, x, j;
  x = id.split(' ')
  a = []
  for (j = 0; j < x.length; j++) {
    a.push(document.getElementById(x[j]))
  };

  for (i = 0; i < a.length; i++) {
    b = a[i].getElementsByClassName(sel);
    for (ii = 0; ii < b.length; ii++) {
      hit = 0;
      d = b[ii].getElementsByClassName(sel_where)
      for (iiii = 0; iiii < d.length; iiii++) {
        if (d[iiii].innerHTML.toUpperCase().indexOf(filter.toUpperCase()) > -1) {
        hit = 1;
        }
        c = d[iiii].getElementsByTagName("*");
        for (iii = 0; iii < c.length; iii++) {
            if (c[iii].innerHTML.toUpperCase().indexOf(filter.toUpperCase()) > -1) {
                hit = 1;
            }
        }
      }
      if (hit == 1) {
        b[ii].style.display = "";
      } else {
        b[ii].style.display = "none";
      }
    }
  }
};

function sortHTML (id, sel, sortvalue) {
    //id - елемент-родитель
    //sel - елемент который подвергнется сортировке
    //sortvalue - елемент где находится текст для сортировки

    var a, b, i, ii, j;
    a = document.getElementById(id);
    b = a.querySelectorAll(sel)
    b = Array.prototype.slice.call(b);
    b.sort(function(a, b){
        i = a.querySelector(sortvalue);
        i = i.textContent;
        i = i.trim();
        i = i.toLowerCase();

        ii = b.querySelector(sortvalue);
        ii = ii.textContent;
        ii = ii.trim();
        ii = ii.toLowerCase();

        return i.localeCompare(ii);
    })

    if (!a.asc) {
        a.asc = true;
    } else {
        a.asc = false;
        b.reverse()
    }

    a.innerHTML = ''

    for (j = 0; j < b.length; j++) {
        a.appendChild(b[j])
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setCookie(cname, cvalue, exhours) {
    var d = new Date();
    d.setTime(d.getTime() + (exhours*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function last_alarm_before_signin() {
    var cname = getCookie('family');
    if (cname) {
        var overlay = document.getElementById('signin_modal_container');
        var overlay_content = document.getElementById('signin_modal_content');
        var specialist_id = this.parentElement.parentElement.parentElement.getAttribute('data-id');
        var specialist_name = this.parentElement.parentElement.parentElement.getAttribute('data-fio');
        var specialist_speciality = this.parentElement.parentElement.parentElement.getAttribute('data-speciality');
        var d = new Date(this.getAttribute('data-sign-date'));
        var signin_time = this.getAttribute('data-sign-time');

        document.getElementById('signin_fio').innerHTML = specialist_name;
        document.getElementById('signin_speciality').innerHTML = specialist_speciality;
        document.getElementById('signin_date').innerHTML = d.getDate() + ' ' + full_months[d.getMonth()] + ' (' + full_week_days[d.getDay()] + ')';
        document.getElementById('signin_time').innerHTML = signin_time;
        var r_month = (d.getMonth() < 10) ? '0' + (d.getMonth() + 1) : d.getMonth() + 1;
        var r_date = (d.getDate() < 10) ? '0' + d.getDate() : d.getDate();
        signin_time_button = this;
        signin_request_data = 'specialist_id=' + specialist_id +                   //id врача
                               '&date=' + d.getFullYear() + r_month + r_date + //дата (20171223)
                               '&time=' + signin_time;                              //время (11:20)
        overlay_content.style.display = 'block';
        overlay.style.display = 'block';
    }
    else{
        show_auth_form();
    }
}

function update_zapisy(sign_items) {
    var zapisi = document.getElementById('zapisi');
    var zapisi_items_div = document.getElementById('zapisi_items');
    zapisi_items_div.innerHTML = '';
    if (sign_items) {
        for (var i=0; i < sign_items.length; i++) {
            var panel_div = document.createElement('div');
            panel_div.className = 'w3-panel w3-border w3-round';

            var row_div = document.createElement('div');
            row_div.className = 'w3-cell-row w3-section';

            var cell_div_1 = document.createElement('div');
            cell_div_1.className = 'w3-cell'
            var el_div = document.createElement('div');
            var el_text = document.createTextNode(sign_items[i].sign_specialist_name);
            el_div.appendChild(el_text);
            cell_div_1.appendChild(el_div);

            el_div = document.createElement('div');
            el_text = document.createTextNode(sign_items[i].sign_specialist_role);
            el_div.appendChild(el_text);
            cell_div_1.appendChild(el_div);

            el_div = document.createElement('div');
            el_div.className = 'w3-red w3-tag w3-round';
            el_text = document.createTextNode(sign_items[i].sign_date + ' -- ' + sign_items[i].sign_time);
            el_div.appendChild(el_text);
            cell_div_1.appendChild(el_div);

            var cell_div_2 = document.createElement('div');
            cell_div_2.className = 'w3-cell w3-cell-middle';
            var el_button = document.createElement('button');
            el_text = document.createTextNode('Отменить');
            el_button.appendChild(el_text);
            el_button.className = 'w3-btn w3-teal w3-round';
            el_button.setAttribute('data-id', sign_items[i].id);
            el_button.setAttribute('data-date', sign_items[i].date);
            el_button.setAttribute('data-time', sign_items[i].time);
            el_button.addEventListener('click', sign_out);
            cell_div_2.appendChild(el_button);

            row_div.appendChild(cell_div_1);
            row_div.appendChild(cell_div_2);
            panel_div.appendChild(row_div);
            zapisi_items_div.appendChild(panel_div);
        }
        zapisi.style.display = 'block';
    }
    else{
        zapisi.style.display = 'none';
    }
}


