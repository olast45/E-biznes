package controllers

import (
	"myapp/models"
	"net/http"
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/labstack/echo/v4"
	"github.com/go-playground/validator/v10"
	"gorm.io/gorm"
)

type ProductController struct{}

func (pc *ProductController) GetProductById(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var product models.Product

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&product, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Product with id=%s not found", id),
		})
	}

	return c.JSON(http.StatusOK, product)
}

func (pc *ProductController) GetAllProducts(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	var products []models.Product

	if len := db.Find(&products).RowsAffected ; len == 0 {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": "There are no products to be displayed",
		})
	}

	return c.JSON(http.StatusOK, products)
}

func (pc *ProductController) CreateProduct(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	var product models.Product

	decoder := json.NewDecoder(c.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&product); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Invalid JSON payload",
		})
	}

	if err := validator.New().Struct(&product); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": err.Error(),
		})
	}

	var category models.Category
	
	if product.CategoryID != nil {
		if err := db.First(&category, *product.CategoryID).Error; err != nil {
			return c.JSON(http.StatusNotFound, map[string]string{
				"error": "Category not found",
			})
		}
	}
	

	if err := db.Create(&product).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Could not create product",
		})
	}

	return c.JSON(http.StatusCreated, product)
}

func (pc *ProductController) UpdateProduct(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var product models.Product

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&product, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Product with id=%s not found", id),
		})
	}

	var updates map[string]interface{}
	decoder := json.NewDecoder(c.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&updates); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Invalid JSON payload",
		})
	}

	if categoryID, exists := updates["category_id"]; exists {
		var category models.Category
		if err := db.First(&category, categoryID).Error; err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{
				"error": "Category ID does not exist",
			})
		}
	}

	if err := db.Model(&product).Updates(updates).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to update product",
		})
	}

	return c.JSON(http.StatusOK, product)
}

func (pc *ProductController) DeleteProduct(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var product models.Product

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&product, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Product with id=%s not found", id),
		})
	}

	db.Delete(&product)


	return c.JSON(http.StatusOK, fmt.Sprintf("Product with id=%s deleted", id))
}

func (pc *ProductController) DeleteAllProducts(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	db.Exec("DELETE FROM products")

	return c.JSON(http.StatusOK, "All products deleted!")
}
