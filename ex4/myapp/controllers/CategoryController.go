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

type CategoryController struct{}

func (cc *CategoryController) GetCategoryById(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var category models.Category

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.Preload("Products").First(&category, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Category with id=%s not found", id),
		})
	}

	return c.JSON(http.StatusOK, category)
}


func (cc *CategoryController) GetAllCategories(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	var categories []models.Category

	if err := db.Preload("Products").Find(&categories).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to fetch categories",
		})
	}

	if len(categories) == 0 {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": "There are no categories to be displayed",
		})
	}

	return c.JSON(http.StatusOK, categories)
}


func (cc *CategoryController) CreateCategory(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	var category models.Category

	decoder := json.NewDecoder(c.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&category); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Invalid JSON payload",
		})
	}

	if err := validator.New().Struct(&category); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": err.Error(),
		})
	}

	if err := db.Create(&category).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Could not create category",
		})
	}

	return c.JSON(http.StatusCreated, category)
}

func (cc *CategoryController) UpdateCategory(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var category models.Category

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&category, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Category with id=%s not found", id),
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

	if err := db.Model(&category).Updates(updates).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to update category",
		})
	}

	return c.JSON(http.StatusOK, category)
}

func (cc *CategoryController) DeleteCategory(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var category models.Category

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&category, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Category with id=%s not found", id),
		})
	}

	var count int64
	if err := db.Model(&models.Product{}).
		Where("category_id = ?", id).
		Count(&count).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Could not check category usage",
		})
	}

	if count > 0 {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Cannot delete category: products are still assigned to it",
		})
	}

	db.Delete(&category)


	return c.JSON(http.StatusOK, fmt.Sprintf("Category with id=%s deleted", id))
}

