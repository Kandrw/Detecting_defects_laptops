import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { api } from "./api/api";
import { ReportContainer } from "./widgets/ReportContainer";

interface IDefects {
  Scratches: string;
  BrokenPixels: string;
  ProblemsWithButtons: string;
  Zamok: string;
  MissingScrew: string;
  Chips: string;
}

export const MainPage = () => {
  const [selectedImages, setSelectedImages] = useState<File[]>([]);
  const [serialNumber, setSerialNumber] = useState<string>("");
  const [showAllImages, setShowAllImages] = useState(false);
  const [editedDefectData, setEditedDefectData] = useState<IDefects | null>(
    null
  );
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleDefectChange = (key: keyof IDefects, value: string) => {
    if (editedDefectData) {
      setEditedDefectData({ ...editedDefectData, [key]: value });
    }
  };

  const resetAll = () => {
    setSelectedImages([]);
    setSerialNumber("");
    setEditedDefectData(null);
    setIsSubmitted(false);
    toast.info("Все данные сброшены!");
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const filesArray = Array.from(event.target.files);
      const validImages = filesArray.filter((file) =>
        file.type.startsWith("image/")
      );
      const invalidFiles = filesArray.filter(
        (file) => !file.type.startsWith("image/")
      );

      if (invalidFiles.length > 0) {
        toast.error(
          "Некоторые файлы не являются изображениями и были отклонены!"
        );
      }

      if (validImages.length > 0) {
        setSelectedImages((prevImages) => [...prevImages, ...validImages]);
        toast.success("Изображения загружены успешно!");
      } else if (validImages.length === 0 && invalidFiles.length > 0) {
        toast.error("Вы загрузили только файлы, не являющиеся изображениями!");
      }
    }
  };

  const handleRemoveImage = (index: number) => {
    setSelectedImages((prevImages) => prevImages.filter((_, i) => i !== index));
    toast.info("Изображение удалено!");
  };

  const handleRemoveAllImages = () => {
    setSelectedImages([]);
    toast.info("Все изображения удалены!");
  };

  const handleSubmitImages = async () => {
    if (selectedImages.length === 0) {
      toast.error("Вы не загрузили изображения!");
      return;
    }

    if (!serialNumber) {
      toast.error("Введите серийный номер!");
      return;
    }

    const formData = new FormData();
    selectedImages.forEach((image) => {
      formData.append("images", image);
    });
    formData.append("serial_number", serialNumber);

    try {
      const response = await api.postUpload();
      if (response.status === 200) {
        toast.success("Фотографии отправлены на проверку успешно!");
        setSelectedImages([]);
        setIsSubmitted(true); // Устанавливаем флаг отправки
        setTimeout(async () => {
          const result = await response.data;
          setEditedDefectData(result);
        }, 5000);
      } else {
        toast.error("Ошибка при отправке фотографий!");
      }
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      toast.error("Ошибка сети при отправке фотографий!");
    }
  };

  const handleSubmitReport = async () => {
    try {
      if (!editedDefectData) {
        toast.error("Нет данных о дефектах для отправки!");
        return;
      }
      const response = await api.postReport(serialNumber, editedDefectData);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "report.docx");
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      toast.error("Ошибка при отправке отчета!");
    }
  };

  const visibleImages = showAllImages
    ? selectedImages
    : selectedImages.slice(0, 5);

  return (
    <div className="relative pt-[2rem]">
      <button
        className="absolute top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
        onClick={resetAll}
      >
        Новый ноутбук
      </button>

      {!isSubmitted ? (
        <div className="max-w-md mx-auto p-6 bg-white border border-gray-300 rounded-lg shadow-lg text-center">
          <h2 className="text-2xl font-bold mb-4">Загрузите свои фотографии</h2>

          <input
            type="file"
            multiple
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer inline-block w-[15rem] px-6 py-2 mb-4 bg-green-500 text-white rounded-md hover:bg-green-600"
          >
            Загрузить изображения
          </label>

          {selectedImages.length > 0 && (
            <button
              className="px-6 py-2 mb-4 w-[15rem] bg-red-500 text-white rounded-md hover:bg-red-600"
              onClick={handleRemoveAllImages}
            >
              Удалить все изображения
            </button>
          )}

          <div>
            {selectedImages.length > 5 && (
              <button
                className="text-blue-500 underline mb-4"
                onClick={() => setShowAllImages(!showAllImages)}
              >
                {showAllImages
                  ? "Свернуть"
                  : `Показать все (${selectedImages.length})`}
              </button>
            )}
          </div>

          <div className="flex flex-wrap justify-center gap-4 mb-4">
            {selectedImages.length > 0 ? (
              visibleImages.map((image, index) => (
                <div key={index} className="relative group w-24 h-24">
                  <img
                    src={URL.createObjectURL(image)}
                    alt={`Preview ${index + 1}`}
                    className="w-full h-full object-cover rounded-lg shadow-md"
                  />
                  <button
                    onClick={() => handleRemoveImage(index)}
                    className="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    ×
                  </button>
                </div>
              ))
            ) : (
              <p className="text-gray-500">Фотографии не выбраны</p>
            )}
          </div>

          <input
            type="text"
            placeholder="Введите серийный номер"
            value={serialNumber}
            onChange={(e) => setSerialNumber(e.target.value)}
            className="block w-full mb-4 p-2 border rounded-md"
          />

          <button
            className="px-6 py-2 w-full bg-blue-500 text-white rounded-md hover:bg-blue-600"
            onClick={handleSubmitImages}
          >
            Отправить фотографии на проверку
          </button>
        </div>
      ) : (
        <div className="flex flex-row items-start justify-center">
          {editedDefectData && (
            <div className="mt-4 p-4 bg-gray-100 rounded-md flex flex-col items-center">
              <h3 className="text-xl font-bold mb-2">Результаты проверки</h3>
              <ReportContainer
                defectsData={editedDefectData}
                onDefectChange={handleDefectChange}
              />

              <button
                className="px-6 py-2 mt-4 bg-green-500 text-white rounded-md hover:bg-green-600"
                onClick={handleSubmitReport}
              >
                Получить отчет
              </button>
            </div>
          )}
        </div>
      )}

      <ToastContainer />
    </div>
  );
};
