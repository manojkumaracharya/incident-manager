//https://mdbootstrap.com/docs/jquery/tables/editable/
$(document).ready(function(){
  getData();    
  
})

var {PythonShell} = require('python-shell')
var path = require("path")

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

function processOutput(jsonString){
    //console.log(jsonString);
    var rows = JSON.parse(jsonString);  
    var html='<table class="table table-striped table-bordered" style="font-size:smaller" id="display-table"> '
    html += '<thead> <tr> <th class="th-sm">Incident</th> <th class="th-sm">Summary</th> '
    html += '<th class="th-sm">Open Date</th> <th class="th-sm">Priority</th> <th class="th-sm">Status</th> <th class="th-sm">Last Updated</th> '
    html += '<th class="th-sm">Updated By</th><th class="th-sm">Slack Channel</th> </tr> </thead> <tbody>'

    for (var i=0;i<rows.length;i++){
      html+= '<tr> <th class="pt-3-half" >' + rows[i].IN_NO + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].SUMMARY + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].OPEN_DATE + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].PRIORITY + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].STATUS + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].LAST_UPDATED + '</td> '
      html+= '<td class="pt-3-half" >' + rows[i].UPDATED_BY + '</td> '
      // html+= '<td><button type="button" class="btn btn-danger btn-rounded btn-sm my-0">Create Slack Channel</button></td> </tr>'
      html+= '<td><span class="table-add float-right mb-3 mr-2"><a href="#!" class="text-success"><i class="fa fa-plus fa-2x" aria-hidden="true"></i></a></span></td> </tr>'
    }
    html += '</tbody> <tfoot> <tr><th>Incident</th><th>Summary</th><th>Open Date</th><th>Priority</th><th>Status</th><th>Last Updated</th><th>Updated By</th><th>Action</th></tr></tfoot> </table>'
    document.getElementById('editableTable').innerHTML = html; 
}

var { remote } = require('electron');

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
            localStorage.setItem("status",rowSelected.cells[4].innerHTML);
            localStorage.setItem("lastUpdated",rowSelected.cells[5].innerHTML);
            localStorage.setItem("updatedBy",rowSelected.cells[6].innerHTML);
            //alert(msg);
            document.getElementById("editData").disabled = false;
        }
    }
}