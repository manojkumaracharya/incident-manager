var {PythonShell} = require('python-shell')
var path = require("path")
var { remote } = require('electron');

//https://mdbootstrap.com/docs/jquery/tables/editable/
$(document).ready(function(){
  getData();
})

function startSlackChannel(incidentNumber){
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : ['createChannel',incidentNumber]
  }
  //alert(options)
  var pyshell = new PythonShell('slack_conver_api.py', options);
  //alert(pyshell)
  var jsonOutput = ''
  pyshell.on('message', function(message) {
    jsonOutput += message;
  })

  pyshell.end(function (err) {
    if (err) throw err;
    console.log(jsonOutput);
  });
}

function getData() {
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : ['getData']
  }
  //alert(options)
  var pyshell = new PythonShell('Hackademy_Incident_Management.py', options);
  //alert(pyshell)
  var jsonOutput = ''
  pyshell.on('message', function(message) {
    jsonOutput += message;
  })

  pyshell.end(function (err) {
    if (err) throw err;
    //console.log('finished');
    processOutput(jsonOutput);
    document.getElementById("editData").disabled = true;
    highlight_row();
  });
}

$('#editableTable').on('click','.slack',function(ele){
    console.log(ele.target.parentNode.parentNode);
    var tr = ele.target.parentNode.parentNode;
    var str = tr.cells[0].textContent
    //console.log(tr.cells[0].textContent);  
    startSlackChannel(str.trim());
});

function processOutput(jsonString){
    //console.log(jsonString);
    var rows = JSON.parse(jsonString);  
    var html='<table class="table table-striped table-bordered" style="font-size:smaller" id="display-table"> '
    html += '<thead> <tr> <th class="th-sm">Incident</th> <th class="th-sm">Summary</th> '
    html += '<th class="th-sm">Open Date</th> <th class="th-sm">Priority</th> <th class="th-sm">Assigned To</th><th class="th-sm">Status</th> <th class="th-sm">Last Updated</th> '
    html += '<th class="th-sm">Updated By</th><th class="th-sm">Slack</th> </tr> </thead> <tbody>'

    for (var i=0;i<rows.length;i++){
      html+= '<tr> <th class="pt-3-half" >' + rows[i].IN_NO + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].SUMMARY + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].OPEN_DATE + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].PRIORITY + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].ASSIGNED_TO + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].STATUS + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].LAST_UPDATED + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].UPDATED_BY + '</td> '
      // html+= '<td><button type="button" class="btn btn-danger btn-rounded btn-sm my-0">Create Slack Channel</button></td> </tr>'
      //html+= '<td><span class="table-add float-right mb-3 mr-2"><a href="#!" class="text-success"><i class="fa fa-plus fa-2x" aria-hidden="true"></i></a></span></td> </tr>'    
      //https://stackoverflow.com/questions/8449358/creating-a-custom-html-button-with-background-image-and-text
      if(rows[i].STATUS == 'Closed'){
        html+= '<td><button disabled class="btn btn-sm slack" title="incident is closed. Cannot create Slack channel" style="background: #ccc url(images/slack.png); padding: 0.4em 1em;no-repeat;height:39px;width:45px"></button></td>'
      }else{
        html+= '<td><button  class="btn btn-sm slack" title="create Slack channel" style="background: #ccc url(images/slack.png); padding: 0.4em 1em;no-repeat;height:39px;width:45px"></button></td>'

      }      
    }
    html += '</tbody>' ;
    //html +=  '<tfoot> <tr><th>Incident</th><th>Summary</th><th>Open Date</th><th>Priority</th><th>Status</th><th>Last Updated</th><th>Updated By</th><th>Action</th></tr></tfoot>';
    html += '</table>';
    document.getElementById('editableTable').innerHTML = html; 
    

    //https://stackoverflow.com/questions/19605078/how-to-use-pagination-on-html-tables
    $('#display-table').after('<div id="nav"></div>');
    var rowsShown = 6;
    var rowsTotal = $('#display-table tbody tr').length;
    var numPages = rowsTotal/rowsShown;

    for(i = 0;i < numPages;i++) {
        var pageNum = i + 1;
        $('#nav').append('<a href="#" rel="'+i+'">'+pageNum+'</a> ');
    }
    $('#display-table tbody tr').hide();
    $('#display-table tbody tr').slice(0, rowsShown).show();
    $('#nav a:first').addClass('active');
    $('#nav a').on('click', function(){
        $('#nav a').removeClass('active');
        $(this).addClass('active');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#display-table tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).
        css('display','table-row').animate({opacity:1}, 300);
    });
}

//https://stackoverflow.com/questions/42900871/how-to-create-a-modal-window-and-load-html-from-render-process
function openModal() {
  let win = new remote.BrowserWindow({
    parent: remote.getCurrentWindow(),
    modal: true
  })
  var theUrl = 'file://' + __dirname + '/modal.html'
  console.log('url', theUrl);
  win.loadURL(theUrl);
}

//https://www.golangprograms.com/highlight-and-get-the-details-of-table-row-on-click-using-javascript.html
function highlight_row() {
    var table = document.getElementById('display-table');
    var cells = table.getElementsByTagName('td')

    for (var i = 0; i < cells.length; i++) {
        // Take each cell
        var cell = cells[i];
        // do something on onclick event for cell
        cell.onclick = function () {
            // Get the row id where the cell exists
            var rowId = this.parentNode.rowIndex;

            var rowsNotSelected = table.getElementsByTagName('tr');
            for (var row = 0; row < rowsNotSelected.length; row++) {
                rowsNotSelected[row].style.backgroundColor = "";
                rowsNotSelected[row].classList.remove('selected');
            }
            var rowSelected = table.getElementsByTagName('tr')[rowId];
            rowSelected.style.backgroundColor = "lightblue";
            rowSelected.className += " selected";

            //msg = 'The ID of the company is: ' + rowSelected.cells[0].innerHTML;
            //msg += '\nThe cell value is: ' + this.innerHTML;

            localStorage.setItem("incident",rowSelected.cells[0].innerHTML);
            localStorage.setItem("summary",rowSelected.cells[1].innerHTML);
            localStorage.setItem("openDate",rowSelected.cells[2].innerHTML);
            localStorage.setItem("priority",rowSelected.cells[3].innerHTML);
            localStorage.setItem("assignedTo",rowSelected.cells[4].innerHTML);
            localStorage.setItem("status",rowSelected.cells[5].innerHTML);
            localStorage.setItem("lastUpdated",rowSelected.cells[6].innerHTML);
            localStorage.setItem("updatedBy",rowSelected.cells[7].innerHTML);
            //alert(msg);
            document.getElementById("editData").disabled = false;
        }
    }
}