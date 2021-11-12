$fecha = Get-Date -Format 'dd_MM_yyyy'
$hora = Get-Date -Format 'HH_mm'
$segundo = Get-Date -UFormat '%s'

Write-Host 'Ingrese una URL para Web Scraping'
$url = Read-Host 'URL'

try{
    Write-Host ''

    $response = Invoke-WebRequest $url

    if($response.StatusCode -eq 200){
        Write-Host 'Comunicacion Exitosa'
        Write-Host 'Iniciando Web Scraping'
        Write-Host ''

        # ---<=> WEB SCRAPING - HTML <=>---
        $carpeta = Test-Path '.\Web_Scraping'
        if($carpeta -eq $True){
            Write-Host 'Directorio Existente'
        }
        else{
            New-Item Web_Scraping -Type Directory
        }

        $carpeta_Web = '.\Web_Scraping\' + $url + '_' + $fecha + '_' + $hora + '_' + $segundo
        $prueba_Carpeta_Web = Test-Path $carpeta_Web
        if($prueba_Carpeta_Web -eq $True){
            Write-Host 'Directorio Existente'
        }
        else{
            New-Item $carpeta_Web -Type Directory
        }

        $direccion = $carpeta_Web + '\' + 'source_code.txt'
        $prueba_direccion = Test-Path $direccion
        if($prueba_direccion -eq $True){
            Write-Host 'Archivo Existente'
        }
        else{
            New-Item -Path $direccion
            $contenido = $response.content
            $contenido >> $direccion
        }

        # ---<=> WEB SCRAPING - JSON <=>---
        $decode = ConvertTo-Json -InputObject $response.content
        $direccion_JSON = $carpeta_Web + '\ ' + 'Json_file.json'
        $prueba_direccion_JSON = Test-Path $direccion_JSON
        if($prueba_direccion_JSON -eq $True){
            Write-Host 'Archivo Existente'
        }
        else{
            New-Item -Path $direccion_JSON
            $contenido_JSON = $decode
            $contenido_JSON >> $direccion_JSON
        }

        # ---<=> WEB SCRAPING - IMAGENES <=>---
        $carpeta_Imagen_Web = $carpeta_Web + '\Imagenes'
        $prueba_Carpeta_Imagen_Web = Test-Path $carpeta_Imagen_Web
        if($prueba_Carpeta_Imagen_Web -eq $True){
            Write-Host 'Directorio Existente'
        }
        else{
            New-Item $carpeta_Imagen_Web -Type Directory
        }

        $images = $response.Images.src

        $direccion_Image = $carpeta_Web + '\ ' + 'images.txt'
        $prueba_direccion_Image = Test-Path $direccion_Image
        if($prueba_direccion_Image -eq $True){
            Write-Host 'Archivo Existente'
        }
        else{
            foreach($image in $images){
                $name = $image
                $name >> $direccion_Image
            }
        }

        $i = 0
        foreach($image in $images){
            $name = $image
            $path = $carpeta_Imagen_Web + '\' + $url + '_' + $i + '.jpg'
            try{
                Invoke-WebRequest $name -OutFile ($path)
            }
            catch{
                Write-Host 'No se pudo Descargar la Imagen'
            }

            $i = $i + 1
        }
    }
    else{
        Write-Host 'No se pudo Conectar a la Pagina'
    }

}
catch{
    Write-Host 'No se pudo Conectar a la Pagina'
}
