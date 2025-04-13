package routes

import (
	"myapp/controllers"

	"github.com/labstack/echo/v4"
)

func ProductRoutes(e *echo.Echo) {

	var controller controllers.ProductController

	e.GET("/products/:id", controller.GetProductById)
	e.GET("/products", controller.GetAllProducts)
	e.POST("/products", controller.CreateProduct)
	e.PUT("/products/:id", controller.UpdateProduct)
	e.DELETE("/products/:id", controller.DeleteProduct)
	e.DELETE("/products", controller.DeleteAllProducts)
}
