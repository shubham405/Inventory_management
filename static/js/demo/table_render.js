const excel_file = document.getElementById('excel_file');

        excel_file.addEventListener('change', (event) => {
            if (!['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'].includes(event.target.files[0].type)) {
                document.getElementById('excel_data').innerHTML = '<div class="alert alert-danger">Only .xlsx or .xls file format is allowed</div>';
                excel_file.value = '';
                return false;
            }

            var reader = new FileReader();

            reader.readAsArrayBuffer(event.target.files[0]);

            reader.onload = function(event){
                var data = new Uint8Array(reader.result);
                var work_book = XLSX.read(data, {type:'array'});
                var sheet_name = work_book.SheetNames;
                var sheet_data = XLSX.utils.sheet_to_json(work_book.Sheets[sheet_name[0]], {header:1});

                var col = [];

                if (sheet_data.length > 0) {
                    var table_output = '<div id="excel_data" class="mt-5 table-responsive">\n<table class="table table-striped table-bordered" id="test" style="overflow-x: scroll;"  cellspacing="0">';
                    
                    for (var row = 0; row < sheet_data.length; row++) {
                        if(row!=0)
                        table_output += '<tr>';
                        
                        for (var cell = 0; cell < sheet_data[0].length; cell++) {
                            if (row === 0) {
                                // Header row
                                col.push({ title: sheet_data[row][cell] });
                                //table_output += '<th>'+sheet_data[row][cell]+'</th>';
                            } else {
                                // Data rows
                                table_output += '<td>'+sheet_data[row][cell]+'</td>';
                            }
                        }
                        if(row)
                        table_output += '</tr>';
                    }

                    table_output += '</table></div>';

                    document.getElementById('excel_data').innerHTML = table_output;

                    // Initialize DataTable inside a setTimeout to ensure the table is fully rendered
                    setTimeout(function() {
                        $('#test').DataTable({
                            "paging": true,
                            "searching": true,
                            "ordering": true,
                            "info": true,
                            "columns": col,
                             // Default sorting on the first column
                           // Keep the first row constant in ascending order
                        });
                          
                    }, 100);
                }

                excel_file.value = '';
            };
        });