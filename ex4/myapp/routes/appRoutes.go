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

func CartRoutes(e *echo.Echo) {

	var controller controllers.CartController

	e.GET("/carts/:id", controller.GetCartById)
	e.GET("/carts", controller.GetAllCarts)
	e.POST("/carts", controller.CreateCart)
	e.PUT("/carts/:id", controller.UpdateCart)
	e.DELETE("/carts/:id", controller.DeleteCart)
	e.DELETE("/carts", controller.DeleteAllCarts)
}

func CategoryRoutes(e *echo.Echo) {

	var controller controllers.CategoryController

	e.GET("/categories/:id", controller.GetCategoryById)
	e.GET("/categories", controller.GetAllCategories)
	e.POST("/categories", controller.CreateCategory)
	e.PUT("/categories/:id", controller.UpdateCategory)
	e.DELETE("/categories/:id", controller.DeleteCategory)

}
