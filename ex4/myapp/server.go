package main

import (
	"myapp/routes"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"myapp/models"

	"github.com/labstack/echo/v4"
)

func ConnectToDatabase() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{})

	if err != nil {
		panic("Failed to connect with the database")
	}

	db.AutoMigrate(&models.Product{})

	return db

}

func main() {
	e := echo.New()
	db := ConnectToDatabase()

	e.Use(func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			c.Set("db", db)
			return next(c)
		}
	})
	

	routes.ProductRoutes(e)

	e.Logger.Fatal(e.Start(":1323"))
}
