import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)

#TODO: 
# Bakılanlara tik işareti konulsun ui-map kısmında.
# Adress aramasını ilk önce depremin merkez üssü ve etrafında ki illeri kapsayarak yap, komşu illere ve depremin merkez iline öncelik ver.