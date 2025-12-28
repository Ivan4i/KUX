import { useState } from 'react'
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
  DragStartEvent,
  DragOverlay,
} from '@dnd-kit/core'
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import { FaPlus, FaPlay, FaPause, FaStop, FaSave, FaClock } from 'react-icons/fa'
import { Button } from '@/components/common/Button'
import { StepCard, StepCardOverlay } from './StepCard'
import { StepEditor } from './StepEditor'
import type { Scenario, ScenarioStep, CreateStepRequest, UpdateStepRequest } from '@/types/scenario'
import { STATUS_CONFIG } from '@/types/scenario'

interface ScenarioBuilderProps {
  scenario: Scenario
  onUpdateScenario: (data: { name?: string; description?: string }) => Promise<void>
  onAddStep: (data: CreateStepRequest) => Promise<void>
  onUpdateStep: (stepId: string, data: UpdateStepRequest) => Promise<void>
  onDeleteStep: (stepId: string) => Promise<void>
  onReorderSteps: (stepIds: string[]) => Promise<void>
  onRun: () => Promise<void>
  onPause: () => Promise<void>
  onResume: () => Promise<void>
  onCancel: () => Promise<void>
  onSchedule: (cron: string) => Promise<void>
  onBack: () => void
  isLoading?: boolean
}

export function ScenarioBuilder({
  scenario,
  onUpdateScenario,
  onAddStep,
  onUpdateStep,
  onDeleteStep,
  onReorderSteps,
  onRun,
  onPause,
  onResume,
  onCancel,
  onSchedule,
  onBack,
  isLoading = false,
}: ScenarioBuilderProps) {
  const [steps, setSteps] = useState<ScenarioStep[]>(scenario.steps)
  const [activeId, setActiveId] = useState<string | null>(null)
  const [editingStep, setEditingStep] = useState<ScenarioStep | null>(null)
  const [isStepEditorOpen, setIsStepEditorOpen] = useState(false)
  const [isEditingName, setIsEditingName] = useState(false)
  const [editedName, setEditedName] = useState(scenario.name)
  const [editedDescription, setEditedDescription] = useState(scenario.description || '')
  const [showScheduleModal, setShowScheduleModal] = useState(false)
  const [cronExpression, setCronExpression] = useState(scenario.cron_expression || '')

  const statusConfig = STATUS_CONFIG[scenario.status]
  const isRunning = scenario.status === 'running'
  const isPaused = scenario.status === 'paused'
  const canRun = ['draft', 'completed', 'failed', 'cancelled'].includes(scenario.status)

  // Update steps when scenario changes
  useState(() => {
    setSteps(scenario.steps)
  })

  // DnD sensors
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  )

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string)
  }

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event

    if (over && active.id !== over.id) {
      const oldIndex = steps.findIndex((s) => s.id === active.id)
      const newIndex = steps.findIndex((s) => s.id === over.id)

      const newSteps = arrayMove(steps, oldIndex, newIndex)
      setSteps(newSteps)

      // Save new order to backend
      await onReorderSteps(newSteps.map((s) => s.id))
    }

    setActiveId(null)
  }

  const activeStep = activeId ? steps.find((s) => s.id === activeId) : null
  const activeIndex = activeId ? steps.findIndex((s) => s.id === activeId) : -1

  const handleAddStep = () => {
    setEditingStep(null)
    setIsStepEditorOpen(true)
  }

  const handleEditStep = (step: ScenarioStep) => {
    setEditingStep(step)
    setIsStepEditorOpen(true)
  }

  const handleSaveStep = async (data: CreateStepRequest | UpdateStepRequest) => {
    if (editingStep) {
      await onUpdateStep(editingStep.id, data as UpdateStepRequest)
    } else {
      await onAddStep(data as CreateStepRequest)
    }
    setIsStepEditorOpen(false)
    setEditingStep(null)
  }

  const handleDeleteStep = async (stepId: string) => {
    if (window.confirm('Are you sure you want to delete this step?')) {
      await onDeleteStep(stepId)
      setSteps((prev) => prev.filter((s) => s.id !== stepId))
    }
  }

  const handleSaveName = async () => {
    await onUpdateScenario({ name: editedName, description: editedDescription })
    setIsEditingName(false)
  }

  const handleScheduleSave = async () => {
    if (cronExpression) {
      await onSchedule(cronExpression)
    }
    setShowScheduleModal(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={onBack}
                className="text-gray-500 hover:text-gray-700"
              >
                ← Back
              </button>

              {isEditingName ? (
                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    value={editedName}
                    onChange={(e) => setEditedName(e.target.value)}
                    className="text-xl font-bold border-b-2 border-primary-500 focus:outline-none"
                    autoFocus
                  />
                  <Button size="sm" onClick={handleSaveName} isLoading={isLoading}>
                    <FaSave className="w-4 h-4" />
                  </Button>
                </div>
              ) : (
                <h1
                  className="text-xl font-bold text-gray-900 cursor-pointer hover:text-primary-600"
                  onClick={() => setIsEditingName(true)}
                >
                  {scenario.name}
                </h1>
              )}

              <span className={`px-2.5 py-1 text-xs font-medium rounded-full ${statusConfig.bgColor} ${statusConfig.color}`}>
                {statusConfig.label}
              </span>
            </div>

            <div className="flex items-center gap-2">
              {canRun && (
                <Button
                  variant="primary"
                  size="sm"
                  leftIcon={<FaPlay className="w-3 h-3" />}
                  onClick={onRun}
                  isLoading={isLoading}
                  disabled={steps.length === 0}
                >
                  Run
                </Button>
              )}

              {isRunning && (
                <>
                  <Button
                    variant="secondary"
                    size="sm"
                    leftIcon={<FaPause className="w-3 h-3" />}
                    onClick={onPause}
                    isLoading={isLoading}
                  >
                    Pause
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    leftIcon={<FaStop className="w-3 h-3" />}
                    onClick={onCancel}
                    isLoading={isLoading}
                  >
                    Cancel
                  </Button>
                </>
              )}

              {isPaused && (
                <>
                  <Button
                    variant="primary"
                    size="sm"
                    leftIcon={<FaPlay className="w-3 h-3" />}
                    onClick={onResume}
                    isLoading={isLoading}
                  >
                    Resume
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    leftIcon={<FaStop className="w-3 h-3" />}
                    onClick={onCancel}
                    isLoading={isLoading}
                  >
                    Cancel
                  </Button>
                </>
              )}

              <Button
                variant="ghost"
                size="sm"
                leftIcon={<FaClock className="w-3 h-3" />}
                onClick={() => setShowScheduleModal(true)}
              >
                Schedule
              </Button>
            </div>
          </div>

          {/* Description */}
          {isEditingName ? (
            <textarea
              value={editedDescription}
              onChange={(e) => setEditedDescription(e.target.value)}
              placeholder="Add a description..."
              className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              rows={2}
            />
          ) : scenario.description ? (
            <p className="mt-2 text-sm text-gray-500 cursor-pointer" onClick={() => setIsEditingName(true)}>
              {scenario.description}
            </p>
          ) : null}
        </div>
      </div>

      {/* Steps Builder */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">
            Steps ({steps.length})
          </h2>
          <Button
            variant="primary"
            size="sm"
            leftIcon={<FaPlus className="w-3 h-3" />}
            onClick={handleAddStep}
          >
            Add Step
          </Button>
        </div>

        {steps.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed border-gray-300">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No steps yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Add your first step to start building the scenario.
            </p>
            <div className="mt-6">
              <Button variant="primary" onClick={handleAddStep}>
                <FaPlus className="w-4 h-4 mr-2" />
                Add First Step
              </Button>
            </div>
          </div>
        ) : (
          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
          >
            <SortableContext items={steps.map((s) => s.id)} strategy={verticalListSortingStrategy}>
              <div className="space-y-3">
                {steps.map((step, index) => (
                  <StepCard
                    key={step.id}
                    step={step}
                    index={index}
                    onEdit={handleEditStep}
                    onDelete={handleDeleteStep}
                    isDragging={activeId === step.id}
                  />
                ))}
              </div>
            </SortableContext>

            <DragOverlay>
              {activeStep ? (
                <StepCardOverlay step={activeStep} index={activeIndex} />
              ) : null}
            </DragOverlay>
          </DndContext>
        )}

        {/* Add Step Button at Bottom */}
        {steps.length > 0 && (
          <div className="mt-4 flex justify-center">
            <button
              onClick={handleAddStep}
              className="flex items-center gap-2 px-4 py-2 text-sm text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
            >
              <FaPlus className="w-3 h-3" />
              Add another step
            </button>
          </div>
        )}
      </div>

      {/* Step Editor Modal */}
      <StepEditor
        isOpen={isStepEditorOpen}
        onClose={() => {
          setIsStepEditorOpen(false)
          setEditingStep(null)
        }}
        onSave={handleSaveStep}
        step={editingStep}
        isLoading={isLoading}
      />

      {/* Schedule Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="fixed inset-0 bg-black bg-opacity-50" onClick={() => setShowScheduleModal(false)} />
          <div className="relative min-h-screen flex items-center justify-center p-4">
            <div className="relative bg-white rounded-xl shadow-xl max-w-md w-full p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Schedule Scenario</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CRON Expression
                  </label>
                  <input
                    type="text"
                    value={cronExpression}
                    onChange={(e) => setCronExpression(e.target.value)}
                    placeholder="0 9 * * * (Every day at 9 AM)"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Format: minute hour day month weekday
                  </p>
                </div>

                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs font-medium text-gray-700 mb-2">Quick presets:</p>
                  <div className="flex flex-wrap gap-2">
                    {[
                      { label: 'Every hour', value: '0 * * * *' },
                      { label: 'Daily 9 AM', value: '0 9 * * *' },
                      { label: 'Mon-Fri 9 AM', value: '0 9 * * 1-5' },
                      { label: 'Weekly Mon', value: '0 9 * * 1' },
                    ].map((preset) => (
                      <button
                        key={preset.value}
                        onClick={() => setCronExpression(preset.value)}
                        className="px-2 py-1 text-xs bg-white border border-gray-200 rounded hover:bg-gray-100"
                      >
                        {preset.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 mt-6">
                <Button variant="secondary" onClick={() => setShowScheduleModal(false)}>
                  Cancel
                </Button>
                <Button variant="primary" onClick={handleScheduleSave} isLoading={isLoading}>
                  Save Schedule
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
